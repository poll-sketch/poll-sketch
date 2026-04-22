import os
import json
import time
import http.client
from urllib.parse import urlparse
from datetime import datetime

LOG_FILE_PATH = r"D:\chat-log\log.txt"

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

def list_directory(directory):
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
        return {"status": "success", "data": items}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def rename_file(old_path, new_name):
    try:
        directory = os.path.dirname(old_path)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        return {"status": "success", "message": f"文件已重命名为: {new_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
                return {"status": "success", "message": f"文件已删除: {file_path}"}
            else:
                return {"status": "error", "message": f"路径不是文件: {file_path}"}
        else:
            return {"status": "error", "message": f"文件不存在: {file_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_file(file_path, content):
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {"status": "success", "message": f"文件已创建: {file_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_file(file_path):
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"status": "success", "data": content}
        else:
            return {"status": "error", "message": f"文件不存在或不是文件: {file_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def append_to_file(file_path, content):
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)

        return {"status": "success", "message": f"内容已追加到: {file_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def fetch_webpage(url, method="GET", headers=None, data=None):
    try:
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path or '/'
        if parsed_url.query:
            path += '?' + parsed_url.query

        request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        if headers:
            request_headers.update(headers)

        if parsed_url.scheme == 'https':
            conn = http.client.HTTPSConnection(host, timeout=30)
        else:
            conn = http.client.HTTPConnection(host, timeout=30)

        conn.request(method, path, body=data, headers=request_headers)

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
        return {"status": "error", "message": str(e)}

def read_chat_log():
    result = read_file(LOG_FILE_PATH)
    if result["status"] == "success":
        return result["data"]
    return ""

tools = {
    "list_directory": list_directory,
    "rename_file": rename_file,
    "delete_file": delete_file,
    "create_file": create_file,
    "read_file": read_file,
    "fetch_webpage": fetch_webpage,
    "read_chat_log": read_chat_log
}

system_prompt = """
你是一个AI助手，拥有以下工具调用能力：

1. list_directory(directory): 列出目录下的文件和子目录
   参数：directory - 目录路径
   返回：包含文件信息的列表

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

6. fetch_webpage(url, method="GET", headers=None, data=None): 访问网页
   参数：url - 访问的URL，method - 请求方法，headers - 请求头，data - 请求数据
   返回：网页内容

7. read_chat_log(): 读取聊天历史记录
   当用户使用/search命令或表达查找聊天历史的意思时，自动调用此工具
   返回：D:\\chat-log\\log.txt文件中的所有聊天历史记录

当用户使用/search开头或表达查找聊天历史的意思时，你应该调用read_chat_log工具获取历史记录，
然后结合历史记录和用户请求进行回复。

工具调用格式示例：
{
  "tool_calls": [
    {
      "name": "工具名称",
      "params": {
        "参数1": "值1"
      }
    }
  ]
}
"""

extract_5w_prompt = """
请从以下聊天记录中提取关键信息，使用5W规则：
- Who（谁）：主要参与者
- What（做了什么事）：主要事件或行动
- When（什么时候，可选）：时间信息
- Where（在何处，可选）：地点信息
- Why（为什么，可选）：原因或目的

每条记录格式：
[时间戳] Who: xxx | What: xxx | When: xxx | Where: xxx | Why: xxx

聊天记录：
{chat_history}

请提取所有关键信息，格式严格要求，每条记录占一行。
"""

summarize_prompt = """
请对以下聊天记录进行总结，保留对话的核心内容和关键信息。

聊天记录：
{chat_history}

总结要求：
1. 用简洁的语言概括对话的主要内容
2. 保留重要的信息和决策
3. 忽略无关的细节
"""

def call_llm_with_tools(env_vars, messages):
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', '')
    temperature = float(env_vars.get('TEMPERATURE', 1))
    max_tokens = int(env_vars.get('MAX_TOKENS', 1000))
    timeout = int(env_vars.get('TIMEOUT', 30))

    if not api_key:
        print("错误：API_KEY未配置")
        return None

    parsed_url = urlparse(base_url)
    host = parsed_url.netloc
    path = parsed_url.path or '/'

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    start_time = time.time()

    try:
        if parsed_url.scheme == 'https':
            conn = http.client.HTTPSConnection(host, timeout=timeout)
        else:
            conn = http.client.HTTPConnection(host, timeout=timeout)

        conn.request("POST", f"{path}/chat/completions", body=json.dumps(data), headers=headers)

        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        conn.close()

        end_time = time.time()
        elapsed_time = end_time - start_time

        result = json.loads(response_data)

        usage = result.get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', 0)
        token_speed = total_tokens / elapsed_time if elapsed_time > 0 else 0

        print("\n=== 统计信息 ===")
        print(f"模型: {model}")
        print(f"耗时: {elapsed_time:.2f}秒")
        print(f"提示词token: {prompt_tokens}")
        print(f"回复token: {completion_tokens}")
        print(f"总token: {total_tokens}")
        print(f"速度: {token_speed:.2f} token/s")
        print("===============")

        return result

    except Exception as e:
        print(f"错误: {e}")
        return None

def process_tool_calls(tool_calls):
    tool_results = []

    for tool_call in tool_calls:
        tool_name = tool_call.get('name')
        params = tool_call.get('params', {})

        if tool_name in tools:
            try:
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
                elif tool_name == "fetch_webpage":
                    result = tools[tool_name](params.get('url'), params.get('method', 'GET'), params.get('headers'), params.get('data'))
                elif tool_name == "read_chat_log":
                    result = tools[tool_name]()
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

def calculate_chat_length(chat_history):
    length = 0
    for message in chat_history:
        if 'content' in message:
            length += len(message['content'])
    return length

def calculate_chat_turns(chat_history):
    turns = 0
    for message in chat_history:
        if message['role'] == 'user':
            turns += 1
    return turns

def extract_5w_info(env_vars, chat_history):
    user_messages = [msg for msg in chat_history if msg['role'] != 'system']

    chat_text = ""
    for msg in user_messages:
        role = "用户" if msg['role'] == 'user' else "AI"
        chat_text += f"{role}: {msg['content']}\n"

    extract_messages = [
        {"role": "system", "content": "你是一个信息提取专家，擅长从聊天记录中提取关键信息。"},
        {"role": "user", "content": extract_5w_prompt.format(chat_history=chat_text)}
    ]

    print("\n正在提取5W关键信息...")
    extract_result = call_llm_with_tools(env_vars, extract_messages)

    if extract_result:
        choices = extract_result.get('choices', [])
        if choices:
            extracted_info = choices[0].get('message', {}).get('content', '')
            print("5W信息提取完成")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"\n=== {timestamp} ===\n{extracted_info}\n"

            append_to_file(LOG_FILE_PATH, log_entry)
            print(f"已保存到: {LOG_FILE_PATH}")

            return True

    return False

def should_search_chat_history(user_input):
    if user_input.strip().startswith("/search"):
        return True

    search_keywords = ["查找聊天历史", "搜索聊天记录", "查看之前聊了什么", "历史记录", "以前聊过", "查一下聊天"]
    for keyword in search_keywords:
        if keyword in user_input:
            return True

    return False

def summarize_chat_history(env_vars, chat_history):
    user_messages = [msg for msg in chat_history if msg['role'] != 'system']

    total_messages = len(user_messages)
    split_point = int(total_messages * 0.7)

    messages_to_summarize = user_messages[:split_point]
    messages_to_keep = user_messages[split_point:]

    chat_text = ""
    for msg in messages_to_summarize:
        role = "用户" if msg['role'] == 'user' else "AI"
        chat_text += f"{role}: {msg['content']}\n"

    summarize_messages = [
        {"role": "system", "content": "你是一个聊天记录总结助手，擅长提炼对话的核心内容。"},
        {"role": "user", "content": summarize_prompt.format(chat_history=chat_text)}
    ]

    print("\n正在总结聊天记录...")
    summarize_result = call_llm_with_tools(env_vars, summarize_messages)

    if summarize_result:
        choices = summarize_result.get('choices', [])
        if choices:
            summary = choices[0].get('message', {}).get('content', '')
            print("聊天记录总结完成")

            new_chat_history = [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": f"【聊天记录总结】{summary}"}
            ]

            new_chat_history.extend(messages_to_keep)

            return new_chat_history

    return chat_history

def chat_loop():
    env_vars = load_env()

    chat_history = [
        {"role": "system", "content": system_prompt}
    ]

    chat_turn_count = 0

    print("===================================")
    print("AI智能体聊天记录5W提取终端")
    print("输入消息开始聊天，按Ctrl+C退出")
    print("支持的工具：列出目录、修改文件名、删除文件、新建文件、读取文件、curl网络访问")
    print("当聊天超过5轮或上下文长度超过3k时，会自动总结聊天记录")
    print("每5次聊天会自动提取5W关键信息并保存到D:\\chat-log\\log.txt")
    print("使用/search开头可搜索聊天历史记录")
    print("===================================")

    try:
        while True:
            try:
                user_input = input("\n你: ")
                if not user_input.strip():
                    continue
            except EOFError:
                break

            need_search = should_search_chat_history(user_input)

            if need_search:
                chat_log = read_chat_log()
                if chat_log:
                    search_messages = [
                        {"role": "system", "content": "你是一个聊天历史搜索助手。根据用户提供的聊天历史记录，回答用户的问题。"},
                        {"role": "user", "content": f"以下是用户的聊天历史记录：\n{chat_log}\n\n用户的问题：{user_input}"}
                    ]
                    result = call_llm_with_tools(env_vars, search_messages)
                    if result:
                        choices = result.get('choices', [])
                        if choices:
                            content = choices[0].get('message', {}).get('content', '')
                            print(f"\nAI: {content}")
                            chat_history.append({"role": "user", "content": user_input})
                            chat_history.append({"role": "assistant", "content": content})
                            continue
                else:
                    print("\nAI: 没有找到聊天历史记录。")
                    continue

            chat_history.append({"role": "user", "content": user_input})

            chat_turns = calculate_chat_turns(chat_history)
            chat_length = calculate_chat_length(chat_history)

            if chat_turns > 5 or chat_length > 3000:
                chat_history = summarize_chat_history(env_vars, chat_history)

            chat_turn_count += 1
            if chat_turn_count % 5 == 0:
                extract_5w_info(env_vars, chat_history)

            result = call_llm_with_tools(env_vars, chat_history)

            if result:
                choices = result.get('choices', [])
                if choices:
                    ai_message = choices[0].get('message', {})

                    tool_calls = ai_message.get('tool_calls', [])

                    if tool_calls:
                        print("\nAI: 正在执行工具调用...")
                        tool_results = process_tool_calls(tool_calls)

                        chat_history.append(ai_message)

                        for tool_result in tool_results:
                            chat_history.append({
                                "role": "tool",
                                "tool_call_id": tool_result.get('tool_call_id'),
                                "name": tool_result.get('tool_name'),
                                "content": json.dumps(tool_result.get('result'))
                            })

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
                        content = ai_message.get('content', '')
                        print(f"\nAI: {content}")
                        chat_history.append(ai_message)

    except KeyboardInterrupt:
        print("\n\n聊天已结束，再见！")

def test_5w_extraction():
    print("=== 测试5W信息提取功能 ===")
    env_vars = load_env()

    test_chat = [
        {"role": "system", "content": "你是一个AI助手"},
        {"role": "user", "content": "我叫张三，今天在成都参加了Python编程培训"},
        {"role": "assistant", "content": "你好张三！成都是个好地方，培训有什么收获吗？"},
        {"role": "user", "content": "我学到了很多关于虚拟环境的知识，还创建了一个项目"},
        {"role": "assistant", "content": "太棒了！虚拟环境是Python开发中非常重要的概念。"}
    ]

    print("测试聊天记录：")
    for msg in test_chat:
        if msg['role'] != 'system':
            role = "用户" if msg['role'] == 'user' else "AI"
            print(f"  {role}: {msg['content']}")

    print("\n提取5W信息...")
    success = extract_5w_info(env_vars, test_chat)

    if success:
        print("5W信息提取测试成功！")
    else:
        print("5W信息提取测试失败！")

def test_search():
    print("\n=== 测试聊天历史搜索功能 ===")

    print("测试1: /search 命令")
    test_input1 = "/search 张三"
    result1 = should_search_chat_history(test_input1)
    print(f"  输入: '{test_input1}' -> 应该搜索: {result1}")

    print("\n测试2: 查找聊天历史")
    test_input2 = "查找聊天历史，看看之前说了什么"
    result2 = should_search_chat_history(test_input2)
    print(f"  输入: '{test_input2}' -> 应该搜索: {result2}")

    print("\n测试3: 普通消息")
    test_input3 = "今天天气真好啊"
    result3 = should_search_chat_history(test_input3)
    print(f"  输入: '{test_input3}' -> 应该搜索: {result3}")

def test_append_file():
    print("\n=== 测试文件追加功能 ===")

    test_content = "\n=== 测试时间 ===\nWho: 测试用户 | What: 测试操作 | When: 测试时间 | Where: 测试地点 | Why: 测试原因\n"

    result = append_to_file(LOG_FILE_PATH, test_content)

    if result["status"] == "success":
        print(f"文件追加成功: {result['message']}")
    else:
        print(f"文件追加失败: {result['message']}")

if __name__ == "__main__":
    test_search()
    test_append_file()
    test_5w_extraction()