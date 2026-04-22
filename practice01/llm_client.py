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

# 使用标准http库访问LLM
def call_llm(env_vars, prompt):
    # 获取配置
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', '')
    temperature = float(env_vars.get('TEMPERATURE', 1))
    max_tokens = int(env_vars.get('MAX_TOKENS', 1000))
    timeout = int(env_vars.get('TIMEOUT', 30))
    
    if not api_key:
        print("错误：API_KEY未配置")
        return None
    
    # 解析URL
    parsed_url = urlparse(base_url)
    host = parsed_url.netloc
    path = parsed_url.path or '/'
    
    # 构建请求数据
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
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
        response_data = response.read().decode('utf-8')
        conn.close()
        
        # 结束计时
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 解析响应
        result = json.loads(response_data)
        
        # 提取token使用情况
        usage = result.get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', 0)
        
        # 计算token/s速度
        token_speed = total_tokens / elapsed_time if elapsed_time > 0 else 0
        
        # 提取回复内容
        choices = result.get('choices', [])
        if choices:
            reply = choices[0].get('message', {}).get('content', '')
        else:
            reply = ""
        
        # 输出统计信息
        print("\n=== LLM调用统计 ===")
        print(f"模型: {model}")
        print(f"耗时: {elapsed_time:.2f}秒")
        print(f"提示词token: {prompt_tokens}")
        print(f"回复token: {completion_tokens}")
        print(f"总token: {total_tokens}")
        print(f"速度: {token_speed:.2f} token/s")
        print("==================")
        print(f"\n回复内容:\n{reply}")
        
        return {
            "reply": reply,
            "elapsed_time": elapsed_time,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "token_speed": token_speed
        }
        
    except Exception as e:
        print(f"错误: {e}")
        return None

if __name__ == "__main__":
    # 加载环境变量
    env_vars = load_env()
    
    # 示例提示词
    prompt = "请解释什么是人工智能，以及它在日常生活中的应用。"
    
    # 调用LLM
    call_llm(env_vars, prompt)