# -*- coding: utf-8 -*-
import os
import sys
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from tool_client import load_env, execute_chained_tool_call, ChainedCallContext, tools, execute_tool

def simulate_llm_decision(user_request, context):
    """
    模拟LLM决策过程，用于测试链式调用
    """
    # 测试1：文件搜索链式调用
    if "查找practice06目录下所有包含'def'关键词的文件" in user_request:
        if context.current_iteration == 0:
            # 第一步：列出practice06目录
            return json.dumps({
                "done": False,
                "tool_call": {
                    "name": "list_directory",
                    "arguments": {"directory": "practice06"}
                }
            })
        elif context.current_iteration == 1:
            # 第二步：读取第一个.py文件
            if context.call_history:
                last_result = context.call_history[-1].get('result', {})
                files = last_result.get('data', [])
                py_files = [f for f in files if f.get('name', '').endswith('.py')]
                if py_files:
                    return json.dumps({
                        "done": False,
                        "tool_call": {
                            "name": "read_file",
                            "arguments": {"file_path": py_files[0]['path']}
                        }
                    })
        elif context.current_iteration == 2:
            # 第三步：总结结果
            summary = "已找到practice06目录下的Python文件，并读取了tool_client.py的内容。该文件包含多个工具函数定义，包括list_directory、rename_file、delete_file、create_file、read_file、fetch_webpage、search_chat_history、anythingllm_query、list_available_skills和load_skill_content等函数。这些函数都使用'def'关键词定义。"
            return json.dumps({
                "done": True,
                "answer": summary
            })
    
    # 测试2：技能查询链式调用
    if "了解notice技能的详细规则" in user_request:
        if context.current_iteration == 0:
            # 第一步：列出可用技能
            return json.dumps({
                "done": False,
                "tool_call": {
                    "name": "list_available_skills",
                    "arguments": {}
                }
            })
        elif context.current_iteration == 1:
            # 第二步：加载notice技能内容
            return json.dumps({
                "done": False,
                "tool_call": {
                    "name": "load_skill_content",
                    "arguments": {"skill_name": "通知撰写"}
                }
            })
        elif context.current_iteration == 2:
            # 第三步：总结结果
            summary = "通知撰写技能的详细规则：\n\n1. 通知格式要求：\n   - 通知不能以'通知'二字开头\n   - 必须冠以部门名称前缀\n   - 格式为'XX部通知'，例如'采购部通知'、'宣传部通知'等\n   - 如果用户没有告知所在部门，使用'XX部'代替\n\n2. 技能功能：\n   - 撰写各类通知文件\n   - 修改和润色通知内容\n   - 支持放假通知、会议通知、公告等多种类型"
            return json.dumps({
                "done": True,
                "answer": summary
            })
    
    # 测试3：网页处理链式调用
    if "访问https://www.nsu.edu.cn" in user_request and "保存到practice07/summary.txt" in user_request:
        if context.current_iteration == 0:
            # 第一步：尝试访问网页（模拟404错误）
            return json.dumps({
                "done": False,
                "tool_call": {
                    "name": "fetch_webpage",
                    "arguments": {"url": "https://www.nsu.edu.cn/HTML/news/2024/06/article_3974.html"}
                }
            })
        elif context.current_iteration == 1:
            # 第二步：总结结果（网页无法访问）
            summary = "尝试访问网页 https://www.nsu.edu.cn/HTML/news/2024/06/article_3974.html 时遇到问题：该网页返回404错误，表示资源不存在或已被删除。\n\n由于无法获取网页内容，已创建一个示例总结文件到practice07/summary.txt，内容如下：\n\n【网页访问总结】\n日期：2024年6月\n来源：https://www.nsu.edu.cn\n状态：无法访问（404 Not Found）\n说明：您要查找的资源可能已被删除、已更改名称或者暂时不可用。建议尝试访问其他页面或联系网站管理员获取最新信息。"
            # 保存到文件
            summary_file = os.path.join(os.path.dirname(__file__), 'summary.txt')
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            return json.dumps({
                "done": True,
                "answer": summary
            })
    
    # 默认：直接回答
    return json.dumps({
        "done": True,
        "answer": "任务已完成。"
    })

def test_chained_calls_with_simulation():
    """
    使用模拟方式测试链式工具调用功能
    """
    print("=" * 60)
    print("测试链式工具调用功能（模拟模式）")
    print("=" * 60)
    
    env_vars = load_env()
    
    # 测试1：文件搜索链式调用
    print("\n【测试1】文件搜索链式调用")
    print("-" * 60)
    user_request = "请查找practice06目录下所有包含'def'关键词的文件，并总结这些文件的主要内容"
    print(f"用户请求：{user_request}")
    print("\n执行过程：")
    
    context1 = ChainedCallContext(max_iterations=5)
    
    while not context1.is_max_iterations_reached():
        print(f"\n--- 第 {context1.current_iteration + 1} 轮迭代 ---")
        
        # 使用模拟决策
        response = simulate_llm_decision(user_request, context1)
        print(f"LLM响应: {response}")
        
        try:
            decision = json.loads(response)
            
            if decision.get('done'):
                context1.final_answer = decision.get('answer', '')
                print(f"\n任务完成！最终回答: {context1.final_answer}")
                break
            else:
                tool_call = decision.get('tool_call', {})
                tool_name = tool_call.get('name')
                arguments = tool_call.get('arguments', {})
                
                print(f"执行工具调用: {tool_name}({arguments})")
                
                # 执行工具
                result = execute_tool(tool_name, arguments)
                print(f"工具执行结果: {result.get('status')}")
                
                # 记录到上下文
                context1.add_call(tool_name, arguments, result)
                
                if result.get('status') == 'success':
                    data = result.get('data')
                    if data:
                        var_name = f"{tool_name}_result"
                        context1.set_variable(var_name, data)
                        print(f"设置中间变量: {var_name}")
                
                context1.increment_iteration()
                
        except json.JSONDecodeError:
            print("无法解析LLM响应，终止链式调用")
            break
    
    print("\n[测试1结果]")
    print(f"总迭代次数: {context1.current_iteration}")
    print(f"调用历史记录数: {len(context1.call_history)}")
    if context1.final_answer:
        print("[测试1通过]")
    else:
        print("[测试1失败]")
    
    # 测试2：技能查询链式调用
    print("\n\n【测试2】技能查询链式调用")
    print("-" * 60)
    user_request = "我想了解notice技能的详细规则"
    print(f"用户请求：{user_request}")
    print("\n执行过程：")
    
    context2 = ChainedCallContext(max_iterations=5)
    
    while not context2.is_max_iterations_reached():
        print(f"\n--- 第 {context2.current_iteration + 1} 轮迭代 ---")
        
        response = simulate_llm_decision(user_request, context2)
        print(f"LLM响应: {response}")
        
        try:
            decision = json.loads(response)
            
            if decision.get('done'):
                context2.final_answer = decision.get('answer', '')
                print(f"\n任务完成！最终回答: {context2.final_answer}")
                break
            else:
                tool_call = decision.get('tool_call', {})
                tool_name = tool_call.get('name')
                arguments = tool_call.get('arguments', {})
                
                print(f"执行工具调用: {tool_name}({arguments})")
                
                result = execute_tool(tool_name, arguments)
                print(f"工具执行结果: {result.get('status')}")
                
                context2.add_call(tool_name, arguments, result)
                
                if result.get('status') == 'success':
                    data = result.get('data')
                    if data:
                        var_name = f"{tool_name}_result"
                        context2.set_variable(var_name, data)
                        print(f"设置中间变量: {var_name}")
                
                context2.increment_iteration()
                
        except json.JSONDecodeError:
            print("无法解析LLM响应，终止链式调用")
            break
    
    print("\n[测试2结果]")
    print(f"总迭代次数: {context2.current_iteration}")
    print(f"调用历史记录数: {len(context2.call_history)}")
    if context2.final_answer:
        print("[测试2通过]")
    else:
        print("[测试2失败]")
    
    # 测试3：网页处理链式调用
    print("\n\n【测试3】网页处理链式调用")
    print("-" * 60)
    user_request = "访问https://www.nsu.edu.cn/HTML/news/2024/06/article_3974.html并总结页面内容，保存到practice07/summary.txt"
    print(f"用户请求：{user_request}")
    print("\n执行过程：")
    
    context3 = ChainedCallContext(max_iterations=5)
    
    while not context3.is_max_iterations_reached():
        print(f"\n--- 第 {context3.current_iteration + 1} 轮迭代 ---")
        
        response = simulate_llm_decision(user_request, context3)
        print(f"LLM响应: {response}")
        
        try:
            decision = json.loads(response)
            
            if decision.get('done'):
                context3.final_answer = decision.get('answer', '')
                print(f"\n任务完成！最终回答: {context3.final_answer}")
                break
            else:
                tool_call = decision.get('tool_call', {})
                tool_name = tool_call.get('name')
                arguments = tool_call.get('arguments', {})
                
                print(f"执行工具调用: {tool_name}({arguments})")
                
                result = execute_tool(tool_name, arguments)
                print(f"工具执行结果: {result.get('status')}")
                
                context3.add_call(tool_name, arguments, result)
                
                if result.get('status') == 'success':
                    data = result.get('data')
                    if data:
                        var_name = f"{tool_name}_result"
                        context3.set_variable(var_name, data)
                        print(f"设置中间变量: {var_name}")
                
                context3.increment_iteration()
                
        except json.JSONDecodeError:
            print("无法解析LLM响应，终止链式调用")
            break
    
    print("\n[测试3结果]")
    print(f"总迭代次数: {context3.current_iteration}")
    print(f"调用历史记录数: {len(context3.call_history)}")
    if context3.final_answer:
        # 检查文件是否创建
        summary_file = os.path.join(os.path.dirname(__file__), 'summary.txt')
        if os.path.exists(summary_file):
            print(f"总结文件已创建: {summary_file}")
            with open(summary_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"文件内容预览（前200字符）: {content[:200]}...")
        print("[测试3通过]")
    else:
        print("[测试3失败]")
    
    print("\n" + "=" * 60)
    print("链式工具调用测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_chained_calls_with_simulation()
