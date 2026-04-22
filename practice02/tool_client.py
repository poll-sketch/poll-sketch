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

# 工具函数1：列出目录文件
def list_directory(directory):
    """
    列出目录下的文件和子目录
    参数：directory - 目录路径
    返回：包含文件信息的列表
    """
    try:
        items = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            item_info = {
                "name": item,
                "path": item_path,
                "type": "directory" if os.path.isdir(item_path) else "file"
            }
            if os.path.isfile(item_path):
                item_info["size"] = os.path.getsize(item_path)
                item_info["mtime"] = os.path.getmtime(item_path)
            items.append(item_info)
        return {
            "status": "success",
            "data": items
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具函数2：修改文件名
def rename_file(old_path, new_name):
    """
    修改文件或目录的名称
    参数：old_path - 原文件/目录路径，new_name - 新名称
    返回：操作结果
    """
    try:
        directory = os.path.dirname(old_path)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        return {
            "status": "success",
            "message": f"文件已重命名为: {new_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具函数3：删除文件
def delete_file(file_path):
    """
    删除文件
    参数：file_path - 文件路径
    返回：操作结果
    """
    try:
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
                return {
                    "status": "success",
                    "message": f"文件已删除: {file_path}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"路径不是文件: {file_path}"
                }
        else:
            return {
                "status": "error",
                "message": f"文件不存在: {file_path}"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具函数4：新建文件并写入内容
def create_file(file_path, content):
    """
    新建文件并写入内容
    参数：file_path - 文件路径，content - 要写入的内容
    返回：操作结果
    """
    try:
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "status": "success",
            "message": f"文件已创建: {file_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具函数5：读取文件内容
def read_file(file_path):
    """
    读取文件内容
    参数：file_path - 文件路径
    返回：文件内容
    """
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "status": "success",
                "data": content
            }
        else:
            return {
                "status": "error",
                "message": f"文件不存在或不是文件: {file_path}"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具函数6：curl网络访问
def curl_request(url, method="GET", headers=None, data=None):
    """
    通过curl访问网页并返回网页内容
    参数：url - 访问的URL，method - 请求方法（默认GET），headers - 请求头，data - 请求数据
    返回：网页内容
    """
    try:
        # 解析URL
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path or '/'
        if parsed_url.query:
            path += '?' + parsed_url.query
        
        # 构建请求头
        request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        if headers:
            request_headers.update(headers)
        
        # 创建连接
        if parsed_url.scheme == 'https':
            conn = http.client.HTTPSConnection(host, timeout=30)
        else:
            conn = http.client.HTTPConnection(host, timeout=30)
        
        # 发送请求
        conn.request(
            method,
            path,
            body=data,
            headers=request_headers
        )
        
        # 接收响应
        response = conn.getresponse()
        content = response.read().decode('utf-8', errors='replace')
        conn.close()
        
        return {
            "status": "success",
            "data": content,
            "status_code": response.status,
            "headers": dict(response.getheaders())
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具映射
tools = {
    "list_directory": list_directory,
    "rename_file": rename_file,
    "delete_file": delete_file,
    "create_file": create_file,
    "read_file": read_file,
    "curl_request": curl_request
}

# 系统提示词
system_prompt = """
你是一个AI助手，拥有以下工具调用能力：

1. list_directory(directory): 列出目录下的文件和子目录
   参数：directory - 目录路径
   返回：包含文件信息的列表，每个文件包含name、path、type等信息

2. rename_file(old_path, new_name): 修改文件或目录的名称
   参数：old_path - 原文件/目录路径，new_name - 新名称
   返回：操作结果

3. delete_file(file_path): 删除文件
   参数：file_path - 文件路径
   返回：操作结果

4. create_file(file_path, content): 新建文件并写入内容
   参数：file_path - 文件路径，content - 要写入的内容
   返回：操作结果

5. read_file(file_path): 读取文件内容
   参数：file_path - 文件路径
   返回：文件内容

6. curl_request(url, method="GET", headers=None, data=None): 通过curl访问网页
   参数：url - 访问的URL，method - 请求方法（默认GET），headers - 请求头，data - 请求数据
   返回：网页内容、状态码和响应头

当用户的请求需要使用这些工具时，你应该生成tool_calls格式的响应，包含工具名称和参数。

工具调用格式示例：
{
  "tool_calls": [
    {
      "name": "工具名称",
      "params": {
        "参数1": "值1",
        "参数2": "值2"
      }
    }
  ]
}

当收到工具执行结果后，你应该将结果用自然语言总结给用户。
"""

# 使用标准http库访问LLM（支持工具调用）
def call_llm_with_tools(env_vars, messages):
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
        "messages": messages,
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
        
        # 输出统计信息
        print("\n=== 统计信息 ===")
        print(f"模型: {model}")
        print(f"耗时: {elapsed_time:.2f}秒")
        print(f"提示词token: {prompt_tokens}")
        print(f"回复token: {completion_tokens}")
        print(f"总token: {total_tokens}")
        print(f"速度: {token_speed:.2f} token/s")
        print("================")
        
        return result
        
    except Exception as e:
        print(f"错误: {e}")
        return None

# 处理工具调用
def process_tool_calls(tool_calls):
    tool_results = []
    
    for tool_call in tool_calls:
        tool_name = tool_call.get('name')
        params = tool_call.get('params', {})
        
        if tool_name in tools:
            try:
                # 调用工具函数
                if tool_name == "list_directory":
                    result = tools[tool_name](params.get('directory'))
                elif tool_name == "rename_file":
                    result = tools[tool_name](params.get('old_path'), params.get('new_name'))
                elif tool_name == "delete_file":
                    result = tools[tool_name](params.get('file_path'))
                elif tool_name == "create_file":
                    result = tools[tool_name](params.get('file_path'), params.get('content'))
                elif tool_name == "read_file":
                    result = tools[tool_name](params.get('file_path'))
                elif tool_name == "curl_request":
                    result = tools[tool_name](
                        params.get('url'),
                        params.get('method', 'GET'),
                        params.get('headers'),
                        params.get('data')
                    )
                else:
                    result = {"status": "error", "message": "未知工具"}
                
                tool_results.append({
                    "tool_call_id": tool_call.get('id'),
                    "tool_name": tool_name,
                    "result": result
                })
                
            except Exception as e:
                tool_results.append({
                    "tool_call_id": tool_call.get('id'),
                    "tool_name": tool_name,
                    "result": {"status": "error", "message": str(e)}
                })
        else:
            tool_results.append({
                "tool_call_id": tool_call.get('id'),
                "tool_name": tool_name,
                "result": {"status": "error", "message": "工具不存在"}
            })
    
    return tool_results

# 主聊天循环
def chat_loop():
    # 加载环境变量
    env_vars = load_env()
    
    # 初始化聊天历史
    chat_history = [
        {"role": "system", "content": system_prompt}
    ]
    
    print("===================================")
    print("AI智能体工具调用终端")
    print("输入消息开始聊天，按Ctrl+C退出")
    print("支持的工具：列出目录、修改文件名、删除文件、新建文件、读取文件")
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
            result = call_llm_with_tools(env_vars, chat_history)
            
            if result:
                # 提取AI回复
                choices = result.get('choices', [])
                if choices:
                    ai_message = choices[0].get('message', {})
                    
                    # 检查是否有工具调用
                    tool_calls = ai_message.get('tool_calls', [])
                    
                    if tool_calls:
                        # 处理工具调用
                        print("\nAI: 正在执行工具调用...")
                        tool_results = process_tool_calls(tool_calls)
                        
                        # 将工具调用添加到聊天历史
                        chat_history.append(ai_message)
                        
                        # 将工具执行结果添加到聊天历史
                        for tool_result in tool_results:
                            chat_history.append({
                                "role": "tool",
                                "tool_call_id": tool_result.get('tool_call_id'),
                                "name": tool_result.get('tool_name'),
                                "content": json.dumps(tool_result.get('result'))
                            })
                        
                        # 再次调用LLM获取最终回复
                        print("\nAI: 正在生成回复...")
                        final_result = call_llm_with_tools(env_vars, chat_history)
                        
                        if final_result:
                            final_choices = final_result.get('choices', [])
                            if final_choices:
                                final_ai_message = final_choices[0].get('message', {})
                                final_content = final_ai_message.get('content', '')
                                print(f"\nAI: {final_content}")
                                chat_history.append(final_ai_message)
                    else:
                        # 直接回复
                        content = ai_message.get('content', '')
                        print(f"\nAI: {content}")
                        chat_history.append(ai_message)
            
            # 限制聊天历史长度
            if len(chat_history) > 20:  # 保留最近20条消息
                chat_history = chat_history[-20:]
                
    except KeyboardInterrupt:
        print("\n\n聊天已结束，再见！")

if __name__ == "__main__":
    chat_loop()