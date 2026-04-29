import os
import json
import time
import http.client
import subprocess
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
    try:
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

# 工具函数6：网络访问
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
        
        conn.request(
            method,
            path,
            body=data,
            headers=request_headers
        )
        
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

# 工具函数7：搜索聊天历史
def search_chat_history(query):
    try:
        log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log.txt')
        
        if not os.path.exists(log_file):
            return {
                "status": "error",
                "message": "聊天历史文件不存在"
            }
        
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        results = []
        
        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                results.append({
                    "line": i + 1,
                    "content": line
                })
        
        return {
            "status": "success",
            "data": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具函数8：AnythingLLM查询
def anythingllm_query(message):
    try:
        env_vars = load_env()
        api_key = env_vars.get('ANYTHINGLLM_API_KEY', '')
        workspace_slug = env_vars.get('ANYTHINGLLM_WORKSPACE_SLUG', '')
        
        if not api_key or not workspace_slug:
            return {
                "status": "error",
                "message": "AnythingLLM API_KEY或WORKSPACE_SLUG未配置"
            }
        
        url = f"http://localhost:3001/api/v1/workspace/{workspace_slug}/chat"
        
        request_data = {
            "message": message
        }
        
        curl_command = [
            "curl",
            "-X", "POST",
            "-H", f"Authorization: Bearer {api_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(request_data),
            url
        ]
        
        result = subprocess.run(
            curl_command,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            return {
                "status": "success",
                "data": response_data.get('response', '')
            }
        else:
            return {
                "status": "error",
                "message": f"请求失败: {result.stderr}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具函数9：读取技能列表
def list_available_skills():
    try:
        skills = []
        project_root = os.path.dirname(__file__)
        skills_dir = os.path.join(project_root, '.agents', 'skills')
        
        if os.path.exists(skills_dir) and os.path.isdir(skills_dir):
            for skill_name in os.listdir(skills_dir):
                skill_dir = os.path.join(skills_dir, skill_name)
                if os.path.isdir(skill_dir):
                    skill_file = os.path.join(skill_dir, 'SKILL.md')
                    if os.path.exists(skill_file) and os.path.isfile(skill_file):
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if content.startswith('---'):
                            front_matter_end = content.find('---', 3)
                            if front_matter_end != -1:
                                front_matter = content[3:front_matter_end].strip()
                                name = ""
                                description = ""
                                for line in front_matter.split('\n'):
                                    line = line.strip()
                                    if line.startswith('name:'):
                                        name = line[5:].strip().strip('"')
                                    elif line.startswith('description:'):
                                        description = line[12:].strip().strip('"')
                                if name:
                                    skills.append({
                                        "name": name,
                                        "description": description
                                    })
        
        return {
            "status": "success",
            "data": skills
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具函数10：读取技能正文
def load_skill_content(skill_name):
    try:
        project_root = os.path.dirname(__file__)
        skills_dir = os.path.join(project_root, '.agents', 'skills')
        
        if not os.path.exists(skills_dir) or not os.path.isdir(skills_dir):
            return {
                "status": "error",
                "message": f"技能目录不存在: {skills_dir}"
            }
        
        for dir_name in os.listdir(skills_dir):
            skill_dir = os.path.join(skills_dir, dir_name)
            if os.path.isdir(skill_dir):
                skill_file = os.path.join(skill_dir, 'SKILL.md')
                if os.path.exists(skill_file) and os.path.isfile(skill_file):
                    with open(skill_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if content.startswith('---'):
                        front_matter_end = content.find('---', 3)
                        if front_matter_end != -1:
                            front_matter = content[3:front_matter_end].strip()
                            for line in front_matter.split('\n'):
                                line = line.strip()
                                if line.startswith('name:'):
                                    current_name = line[5:].strip().strip('"')
                                    if current_name == skill_name:
                                        content = content[front_matter_end + 3:].strip()
                                        return {
                                            "status": "success",
                                            "data": content
                                        }
        
        return {
            "status": "error",
            "message": f"未找到名称为 '{skill_name}' 的技能"
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
    "fetch_webpage": fetch_webpage,
    "search_chat_history": search_chat_history,
    "anythingllm_query": anythingllm_query,
    "list_available_skills": list_available_skills,
    "load_skill_content": load_skill_content
}

# 链式调用上下文管理器
class ChainedCallContext:
    """
    链式调用上下文管理器，用于在多个工具调用之间传递数据和状态
    """
    
    def __init__(self, max_iterations=10):
        """
        初始化链式调用上下文
        参数：max_iterations - 最大迭代次数，防止无限循环
        """
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.call_history = []  # 记录每一步的调用和结果
        self.variables = {}    # 存储中间变量供后续步骤使用
        self.final_answer = None  # 最终回答
    
    def add_call(self, tool_name, arguments, result):
        """
        添加工具调用记录
        参数：
            tool_name - 工具名称
            arguments - 调用参数
            result - 调用结果
        """
        call_record = {
            "iteration": self.current_iteration,
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
            "timestamp": time.time()
        }
        self.call_history.append(call_record)
    
    def set_variable(self, name, value):
        """
        设置中间变量
        参数：
            name - 变量名
            value - 变量值
        """
        self.variables[name] = value
    
    def get_variable(self, name, default=None):
        """
        获取中间变量
        参数：
            name - 变量名
            default - 默认值
        返回：变量值
        """
        return self.variables.get(name, default)
    
    def increment_iteration(self):
        """
        增加迭代次数
        """
        self.current_iteration += 1
    
    def is_max_iterations_reached(self):
        """
        检查是否达到最大迭代次数
        返回：True如果达到最大迭代次数，False否则
        """
        return self.current_iteration >= self.max_iterations
    
    def get_summary(self):
        """
        获取链式调用的摘要信息
        返回：包含调用历史和中间变量的摘要
        """
        return {
            "total_iterations": self.current_iteration,
            "max_iterations": self.max_iterations,
            "call_history": self.call_history,
            "variables": self.variables,
            "final_answer": self.final_answer
        }

# 分析提示词构建函数
def build_analysis_prompt(user_request, context):
    """
    构建分析提示词，用于指导LLM进行链式工具调用决策
    参数：
        user_request - 用户原始请求
        context - ChainedCallContext对象
    返回：构建好的分析提示词
    """
    # 构建已执行步骤历史
    history_text = ""
    if context.call_history:
        history_text = "已执行的步骤历史：\n"
        for i, call in enumerate(context.call_history):
            history_text += f"{i+1}. 工具: {call['tool_name']}\n"
            history_text += f"   参数: {json.dumps(call['arguments'], ensure_ascii=False)}\n"
            result = call['result']
            result_str = json.dumps(result, ensure_ascii=False)
            if len(result_str) > 200:
                result_str = result_str[:200] + "..."
            history_text += f"   结果: {result_str}\n\n"
    
    # 构建中间变量信息
    variables_text = ""
    if context.variables:
        variables_text = "可用的中间变量：\n"
        for name, value in context.variables.items():
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:100] + "..."
            variables_text += f"- {name}: {value_str}\n"
    
    # 构建完整提示词
    prompt = f"""你是一个智能决策助手，负责分析用户请求并决定是否需要调用工具以及调用哪个工具。

用户请求：
{user_request}

{history_text}

{variables_text}

决策规则：
1. 如果你已经获得足够的信息来回答用户的问题，请直接总结回答
2. 如果需要更多信息才能回答用户的问题，请调用适当的工具
3. 可以使用中间变量（如前一步工具的输出）作为后续工具调用的参数
4. 注意避免重复调用相同的工具获取相同的信息
5. 如果任务已经完成，请直接给出最终答案，不需要调用工具

工具列表：
1. list_directory(directory): 列出目录下的文件和子目录
2. rename_file(old_path, new_name): 修改文件或目录的名称
3. delete_file(file_path): 删除文件
4. create_file(file_path, content): 新建文件并写入内容
5. read_file(file_path): 读取文件内容
6. fetch_webpage(url): 访问网页并返回内容
7. search_chat_history(query): 搜索聊天历史记录
8. anythingllm_query(message): 查询AnythingLLM文档仓库
9. list_available_skills(): 读取可用技能列表
10. load_skill_content(skill_name): 加载指定技能的内容

你需要按照以下JSON格式输出决策：

<1>完成任务时：
{{
  "done": true,
  "answer": "最终回答内容"
}}

<2>继续调用工具时:
{{
  "done": false,
  "tool_call": {{
    "name": "工具名称",
    "arguments": {{
      "参数名": "参数值"
    }}
  }}
}}

注意：输出必须是有效的JSON格式，不要包含其他任何内容。
"""
    
    return prompt

# 执行工具调用
def execute_tool(tool_name, arguments):
    """
    执行工具调用
    参数：
        tool_name - 工具名称
        arguments - 工具参数
    返回：工具执行结果
    """
    if tool_name in tools:
        try:
            if tool_name == "list_directory":
                return tools[tool_name](arguments.get('directory'))
            elif tool_name == "rename_file":
                return tools[tool_name](arguments.get('old_path'), arguments.get('new_name'))
            elif tool_name == "delete_file":
                return tools[tool_name](arguments.get('file_path'))
            elif tool_name == "create_file":
                return tools[tool_name](arguments.get('file_path'), arguments.get('content'))
            elif tool_name == "read_file":
                return tools[tool_name](arguments.get('file_path'))
            elif tool_name == "fetch_webpage":
                return tools[tool_name](arguments.get('url'))
            elif tool_name == "search_chat_history":
                return tools[tool_name](arguments.get('query'))
            elif tool_name == "anythingllm_query":
                return tools[tool_name](arguments.get('message'))
            elif tool_name == "list_available_skills":
                return tools[tool_name]()
            elif tool_name == "load_skill_content":
                return tools[tool_name](arguments.get('skill_name'))
            else:
                return {"status": "error", "message": "未知工具"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    else:
        return {"status": "error", "message": "工具不存在"}

# 使用标准http库访问LLM（用于链式调用）
def call_llm_for_chain(env_vars, prompt):
    """
    调用LLM进行链式调用决策
    参数：
        env_vars - 环境变量
        prompt - 提示词
    返回：LLM响应
    """
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', '')
    temperature = float(env_vars.get('TEMPERATURE', 0.1))  # 较低温度用于决策
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
        "messages": [
            {"role": "system", "content": "你是一个智能决策助手，擅长分析用户请求并做出正确的工具调用决策。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        if parsed_url.scheme == 'https':
            conn = http.client.HTTPSConnection(host, timeout=timeout)
        else:
            conn = http.client.HTTPConnection(host, timeout=timeout)
        
        conn.request(
            "POST",
            f"{path}/chat/completions",
            body=json.dumps(data),
            headers=headers
        )
        
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        conn.close()
        
        result = json.loads(response_data)
        
        # 输出统计信息
        usage = result.get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', 0)
        
        print(f"\n[链式调用] 提示词token: {prompt_tokens}, 回复token: {completion_tokens}, 总token: {total_tokens}")
        
        choices = result.get('choices', [])
        if choices:
            return choices[0].get('message', {}).get('content', '')
        
        return None
        
    except Exception as e:
        print(f"[链式调用] 错误: {e}")
        return None

# 链式调用执行函数
def execute_chained_tool_call(env_vars, user_request, max_iterations=10):
    """
    执行链式工具调用的完整流程
    参数：
        env_vars - 环境变量
        user_request - 用户请求
        max_iterations - 最大迭代次数
    返回：最终回答和调用上下文
    """
    print(f"\n=== 开始链式工具调用 ===")
    print(f"用户请求: {user_request}")
    print(f"最大迭代次数: {max_iterations}")
    
    # 初始化链式调用上下文
    context = ChainedCallContext(max_iterations=max_iterations)
    
    # 循环执行链式调用
    while not context.is_max_iterations_reached():
        print(f"\n--- 第 {context.current_iteration + 1} 轮迭代 ---")
        
        # 构建分析提示词
        prompt = build_analysis_prompt(user_request, context)
        
        # 调用LLM决策
        response = call_llm_for_chain(env_vars, prompt)
        
        if not response:
            print("LLM调用失败，终止链式调用")
            break
        
        print(f"LLM响应: {response[:200]}..." if len(response) > 200 else f"LLM响应: {response}")
        
        try:
            # 解析LLM响应
            decision = json.loads(response)
            
            if decision.get('done'):
                # 任务完成
                context.final_answer = decision.get('answer', '')
                print(f"\n任务完成！最终回答: {context.final_answer[:100]}..." if len(context.final_answer) > 100 else f"\n任务完成！最终回答: {context.final_answer}")
                break
            else:
                # 需要继续调用工具
                tool_call = decision.get('tool_call', {})
                tool_name = tool_call.get('name')
                arguments = tool_call.get('arguments', {})
                
                if not tool_name:
                    print("无效的工具调用指令，终止链式调用")
                    break
                
                print(f"执行工具调用: {tool_name}({arguments})")
                
                # 执行工具
                result = execute_tool(tool_name, arguments)
                
                # 记录到上下文
                context.add_call(tool_name, arguments, result)
                
                # 尝试提取有用的中间变量
                if result.get('status') == 'success':
                    data = result.get('data')
                    if data:
                        # 根据工具类型设置不同的变量名
                        var_name = f"{tool_name}_result"
                        context.set_variable(var_name, data)
                        print(f"设置中间变量: {var_name}")
                
                # 增加迭代次数
                context.increment_iteration()
                
        except json.JSONDecodeError:
            print("无法解析LLM响应，终止链式调用")
            break
        except Exception as e:
            print(f"执行过程出错: {e}")
            break
    
    # 检查是否因为达到最大迭代次数而终止
    if context.is_max_iterations_reached():
        print(f"\n达到最大迭代次数({max_iterations})，终止链式调用")
        if not context.final_answer:
            context.final_answer = f"任务未完成，已执行 {max_iterations} 轮工具调用。请检查任务是否过于复杂或增加最大迭代次数。"
    
    print("\n=== 链式调用结束 ===")
    
    return context

# 基础系统提示词
base_system_prompt = """
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

6. fetch_webpage(url, method="GET", headers=None, data=None): 访问网页
   参数：url - 访问的URL，method - 请求方法（默认GET），headers - 请求头，data - 请求数据
   返回：网页内容、状态码和响应头

7. search_chat_history(query): 搜索聊天历史记录
   参数：query - 搜索关键词
   返回：搜索结果

8. anythingllm_query(message): 查询AnythingLLM文档仓库
   参数：message - 查询消息
   返回：仓库中的相关文档信息
   **重要**：当用户提到"文档仓库"、"文件仓库"、"仓库"等关键词时，优先调用此工具

9. list_available_skills(): 读取可用技能列表
   返回：技能列表，每个技能包含name和description字段

10. load_skill_content(skill_name): 加载指定技能的内容
    参数：skill_name - 技能名称
    返回：技能正文内容

【链式工具调用规则】
- 你可以进行链式工具调用，即前一个工具的输出可以作为后一个工具的输入参数
- 系统会自动记录每一步的调用和结果，你可以使用这些中间结果
- 例如：先调用list_directory获取目录列表，再根据结果调用read_file读取特定文件
- 如果任务需要多个步骤完成，请依次调用相应的工具
- 当收集到足够信息后，直接给出最终回答

【链式调用示例】
场景：用户要求"查找practice06目录下所有包含'def'关键词的文件"
步骤1: 调用 list_directory("practice06") 获取文件列表
步骤2: 对每个.py文件调用 read_file(file_path) 读取内容
步骤3: 检查内容是否包含'def'关键词
步骤4: 返回结果

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
        
        conn.request(
            "POST",
            f"{path}/chat/completions",
            body=json.dumps(data),
            headers=headers
        )
        
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

# 处理工具调用
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
                    result = tools[tool_name](
                        params.get('url'),
                        params.get('method', 'GET'),
                        params.get('headers'),
                        params.get('data')
                    )
                elif tool_name == "search_chat_history":
                    result = tools[tool_name](params.get('query'))
                elif tool_name == "anythingllm_query":
                    result = tools[tool_name](params.get('message'))
                elif tool_name == "list_available_skills":
                    result = tools[tool_name]()
                elif tool_name == "load_skill_content":
                    result = tools[tool_name](params.get('skill_name'))
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

# 计算聊天历史的长度（字符数）
def calculate_chat_length(chat_history):
    length = 0
    for message in chat_history:
        if 'content' in message:
            length += len(message['content'])
    return length

# 计算聊天轮数（用户和AI的交互次数）
def calculate_chat_turns(chat_history):
    turns = 0
    for message in chat_history:
        if message['role'] == 'user':
            turns += 1
    return turns

# 总结聊天记录
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
    
    summarize_prompt = """
请对以下聊天记录进行总结，保留对话的核心内容和关键信息，忽略不重要的细节。

聊天记录：
{chat_history}

总结要求：
1. 用简洁的语言概括对话的主要内容
2. 保留重要的信息和决策
3. 忽略无关的细节
4. 总结应该连贯、清晰
"""
    
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
            
            skills_result = list_available_skills()
            skills_json = json.dumps({"skills": skills_result.get('data', [])}, ensure_ascii=False, indent=2)
            
            new_chat_history = [
                {"role": "system", "content": base_system_prompt + "\n\n可用技能列表：\n" + skills_json},
                {"role": "assistant", "content": f"【聊天记录总结】{summary}"}
            ]
            
            new_chat_history.extend(messages_to_keep)
            
            return new_chat_history
    
    return chat_history

# 主聊天循环
def chat_loop():
    env_vars = load_env()
    
    skills_result = list_available_skills()
    skills_json = json.dumps({"skills": skills_result.get('data', [])}, ensure_ascii=False, indent=2)
    
    chat_history = [
        {"role": "system", "content": base_system_prompt + "\n\n可用技能列表：\n" + skills_json}
    ]
    
    print("===================================")
    print("AI智能体链式工具调用终端")
    print("输入消息开始聊天，按Ctrl+C退出")
    print("支持链式工具调用：前一个工具的输出可以作为后一个工具的输入")
    print("支持的工具：列出目录、修改文件名、删除文件、新建文件、读取文件、访问网页、搜索聊天历史、AnythingLLM查询、读取技能列表、加载技能内容")
    print("当聊天超过5轮或上下文长度超过3k时，会自动总结聊天记录")
    print("===================================")
    
    try:
        while True:
            try:
                user_input = input("\n你: ")
                if not user_input.strip():
                    continue
            except EOFError:
                break
            
            # 检查是否需要使用链式调用
            # 如果用户请求涉及多步骤任务，使用链式调用
            if any(keyword in user_input for keyword in ['查找', '搜索', '读取', '总结', '保存', '分析']):
                print("\n检测到需要多步骤处理的请求，使用链式工具调用...")
                context = execute_chained_tool_call(env_vars, user_input)
                
                if context.final_answer:
                    print(f"\nAI: {context.final_answer}")
                    chat_history.append({"role": "user", "content": user_input})
                    chat_history.append({"role": "assistant", "content": context.final_answer})
                else:
                    print("\nAI: 无法完成该请求，请重试")
                continue
            
            skills_result = list_available_skills()
            skills_json = json.dumps({"skills": skills_result.get('data', [])}, ensure_ascii=False, indent=2)
            
            chat_history[0] = {"role": "system", "content": base_system_prompt + "\n\n可用技能列表：\n" + skills_json}
            
            chat_history.append({"role": "user", "content": user_input})
            
            chat_turns = calculate_chat_turns(chat_history)
            chat_length = calculate_chat_length(chat_history)
            
            if chat_turns > 5 or chat_length > 3000:
                chat_history = summarize_chat_history(env_vars, chat_history)
            
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

# 测试链式调用功能
def test_chained_calls():
    """
    测试链式工具调用功能
    """
    print("=== 测试链式工具调用功能 ===")
    
    env_vars = load_env()
    
    # 测试1：文件搜索链式调用
    print("\n【测试1】文件搜索链式调用")
    print("用户请求：请查找practice06目录下所有包含'def'关键词的文件")
    context1 = execute_chained_tool_call(env_vars, "请查找practice06目录下所有包含'def'关键词的文件")
    print(f"最终回答: {context1.final_answer}")
    
    # 测试2：技能查询链式调用
    print("\n【测试2】技能查询链式调用")
    print("用户请求：我想了解notice技能的详细规则")
    context2 = execute_chained_tool_call(env_vars, "我想了解notice技能的详细规则")
    print(f"最终回答: {context2.final_answer}")
    
    # 测试3：网页处理链式调用
    print("\n【测试3】网页处理链式调用")
    print("用户请求：访问https://www.nsu.edu.cn/HTML/news/2024/06/article_3974.html并总结页面内容，保存到practice07/summary.txt")
    context3 = execute_chained_tool_call(env_vars, "访问https://www.nsu.edu.cn/HTML/news/2024/06/article_3974.html并总结页面内容，保存到practice07/summary.txt")
    print(f"最终回答: {context3.final_answer}")
    
    print("\n=== 链式工具调用测试完成 ===")

if __name__ == "__main__":
    # 运行聊天循环
    chat_loop()
    # 运行测试
    # test_chained_calls()
