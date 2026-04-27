import os
import sys
import json
import time
import http.client
from urllib.parse import urlparse

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from tool_client import list_available_skills, load_skill_content, load_env, call_llm_with_tools

def test_skill_integration():
    """
    测试技能管理与LLM集成功能
    """
    print("=" * 60)
    print("测试技能管理与LLM集成")
    print("=" * 60)
    
    # 加载环境变量
    env_vars = load_env()
    
    # 读取技能列表
    print("\n【步骤1】读取技能列表")
    print("-" * 60)
    skills_result = list_available_skills()
    
    if skills_result["status"] == "success":
        skills = skills_result["data"]
        skills_json = json.dumps({"skills": skills}, ensure_ascii=False, indent=2)
        print(f"成功读取到 {len(skills)} 个技能：")
        print(skills_json)
    else:
        print(f"读取失败: {skills_result['message']}")
        return
    
    # 构建系统提示词
    system_prompt = f"""你是一个AI助手，拥有以下工具调用能力：

1. list_available_skills(): 读取可用技能列表
   返回：技能列表，每个技能包含name和description字段

2. load_skill_content(skill_name): 加载指定技能的内容
   参数：skill_name - 技能名称
   返回：技能正文内容

可用技能列表：
{skills_json}

当用户的请求需要使用这些工具时，你应该生成tool_calls格式的响应，包含工具名称和参数。

工具调用格式示例：
{{
  "tool_calls": [
    {{
      "name": "工具名称",
      "params": {{
        "参数1": "值1"
      }}
    }}
  ]
}}

当收到工具执行结果后，你应该将结果用自然语言总结给用户。"""
    
    # 测试1：询问有哪些技能
    print("\n【测试1】询问有哪些技能")
    print("-" * 60)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "请告诉我有哪些可用的技能？"}
    ]
    
    result = call_llm_with_tools(env_vars, messages)
    if result:
        choices = result.get('choices', [])
        if choices:
            ai_message = choices[0].get('message', {})
            content = ai_message.get('content', '')
            print(f"AI回复: {content}")
    
    # 测试2：询问某个技能的详细内容
    print("\n【测试2】询问某个技能的详细内容")
    print("-" * 60)
    if skills:
        skill_name = skills[0]["name"]
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请加载'{skill_name}'技能的详细内容"}
        ]
        
        result = call_llm_with_tools(env_vars, messages)
        if result:
            choices = result.get('choices', [])
            if choices:
                ai_message = choices[0].get('message', {})
                
                # 检查是否有工具调用
                tool_calls = ai_message.get('tool_calls', [])
                
                if tool_calls:
                    print(f"AI决定调用工具: {tool_calls[0].get('name')}")
                    print(f"参数: {tool_calls[0].get('params')}")
                    
                    # 执行工具调用
                    if tool_calls[0].get('name') == 'load_skill_content':
                        skill_name_param = tool_calls[0].get('params', {}).get('skill_name')
                        content_result = load_skill_content(skill_name_param)
                        print(f"\n工具执行结果: {content_result['status']}")
                        if content_result['status'] == 'success':
                            print(f"技能内容（前300字符）:")
                            print(content_result['data'][:300] + "..." if len(content_result['data']) > 300 else content_result['data'])
                else:
                    content = ai_message.get('content', '')
                    print(f"AI回复: {content}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_skill_integration()
