import os
import json
import time
import http.client
from urllib.parse import urlparse

# 读取.env文件
def load_env():
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    env_vars = {}
    
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip('"')
    else:
        print("警告：.env文件不存在，请从env.example复制并填写正确参数")
    
    return env_vars

# 使用标准http库访问LLM（流式输出）
def call_llm_stream(env_vars, messages):
    # 获取配置
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', '')
    temperature = float(env_vars.get('TEMPERATURE', 1))
    max_tokens = int(env_vars.get('MAX_TOKENS', 4096))
    timeout = int(env_vars.get('TIMEOUT', 30))
    
    if not api_key:
        print("错误：API_KEY未配置")
        return None, 0, 0, 0
    
    # 解析URL
    parsed_url = urlparse(base_url)
    host = parsed_url.netloc
    path = parsed_url.path or '/'
    
    # 构建请求数据
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True
    }
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 开始计时
    start_time = time.time()
    
    try:
        # 创建连接
        if parsed_url.scheme == 'https':
            conn = http.client.HTTPSConnection(host, timeout=timeout)
        else:
            conn = http.client.HTTPConnection(host, timeout=timeout)
        
        # 发送请求
        conn.request(
            "POST",
            f"{path}/chat/completions",
            body=json.dumps(data),
            headers=headers
        )
        
        # 接收响应
        response = conn.getresponse()
        
        # 处理流式响应
        reply = ""
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        
        print("\nAI: ", end="", flush=True)
        
        for line in response:
            line = line.decode('utf-8').strip()
            if not line:
                continue
            
            # 处理SSE格式
            if line.startswith('data: '):
                data_part = line[6:]
                if data_part == '[DONE]':
                    break
                
                try:
                    chunk = json.loads(data_part)
                    # 提取回复内容
                    choices = chunk.get('choices', [])
                    if choices:
                        delta = choices[0].get('delta', {})
                        content = delta.get('content', '')
                        if content:
                            print(content, end="", flush=True)
                            reply += content
                    
                    # 提取token使用情况（最后一个chunk）
                    usage = chunk.get('usage', {})
                    if usage:
                        prompt_tokens = usage.get('prompt_tokens', 0)
                        completion_tokens = usage.get('completion_tokens', 0)
                        total_tokens = usage.get('total_tokens', 0)
                except json.JSONDecodeError:
                    pass
        
        print()  # 换行
        conn.close()
        
        # 结束计时
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 计算token/s速度
        token_speed = total_tokens / elapsed_time if elapsed_time > 0 else 0
        
        # 输出统计信息
        print("\n=== 统计信息 ===")
        print(f"模型: {model}")
        print(f"耗时: {elapsed_time:.2f}秒")
        print(f"提示词token: {prompt_tokens}")
        print(f"回复token: {completion_tokens}")
        print(f"总token: {total_tokens}")
        print(f"速度: {token_speed:.2f} token/s")
        print("================")
        
        return reply, prompt_tokens, completion_tokens, total_tokens
        
    except Exception as e:
        print(f"错误: {e}")
        return None, 0, 0, 0

# 主聊天循环
def chat_loop():
    # 加载环境变量
    env_vars = load_env()
    
    # 初始化聊天历史
    chat_history = []
    
    print("===================================")
    print("AI智能体聊天终端")
    print("输入消息开始聊天，按Ctrl+C退出")
    print("===================================")
    
    try:
        while True:
            # 获取用户输入
            try:
                user_input = input("\n你: ")
                if not user_input.strip():
                    continue
            except EOFError:
                break
            
            # 添加用户消息到聊天历史
            chat_history.append({"role": "user", "content": user_input})
            
            # 调用LLM
            reply, _, _, _ = call_llm_stream(env_vars, chat_history)
            
            # 添加AI回复到聊天历史
            if reply:
                chat_history.append({"role": "assistant", "content": reply})
            
            # 限制聊天历史长度（可选）
            if len(chat_history) > 10:  # 保留最近10条消息
                chat_history = chat_history[-10:]
                
    except KeyboardInterrupt:
        print("\n\n聊天已结束，再见！")

if __name__ == "__main__":
    chat_loop()