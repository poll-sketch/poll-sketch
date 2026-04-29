import os
import sys
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from tool_client import list_available_skills, load_skill_content, load_env, call_llm_with_tools

def test_notice_skill():
    """
    测试通知撰写技能
    """
    print("=" * 60)
    print("测试通知撰写技能")
    print("=" * 60)
    
    # 加载环境变量
    env_vars = load_env()
    
    # 读取技能列表
    skills_result = list_available_skills()
    skills_json = json.dumps({"skills": skills_result.get('data', [])}, ensure_ascii=False, indent=2)
    
    # 构建系统提示词，特别强调通知撰写技能的使用
    system_prompt = f"""你是一个AI助手，拥有以下工具调用能力：

1. list_available_skills(): 读取可用技能列表
   返回：技能列表，每个技能包含name和description字段

2. load_skill_content(skill_name): 加载指定技能的内容
   参数：skill_name - 技能名称
   返回：技能正文内容

可用技能列表：
{skills_json}

当用户的请求涉及到通知撰写、修改或润色时，你应该：
1. 首先调用 load_skill_content("通知撰写") 加载通知撰写技能
2. 严格按照技能内容中的格式要求输出通知
3. 如果用户没有告知部门，使用"XX部"作为前缀
4. 如果用户提供了部门名称，使用该部门名称作为前缀

工具调用格式示例：
{{
  "tool_calls": [
    {{
      "name": "load_skill_content",
      "params": {{
        "skill_name": "通知撰写"
      }}
    }}
  ]
}}

当收到工具执行结果后，你应该将结果用自然语言总结给用户，并按照技能要求生成通知内容。"""
    
    # 测试1：用户不提供部门，要求撰写五一节放假通知
    print("\n【测试1】用户不提供部门，要求撰写五一节放假通知")
    print("-" * 60)
    print("用户输入：请帮我撰写一份关于五一节放假的通知")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "请帮我撰写一份关于五一节放假的通知"}
    ]
    
    # 第一次调用：LLM决定是否调用工具
    result = call_llm_with_tools(env_vars, messages)
    if result:
        choices = result.get('choices', [])
        if choices:
            ai_message = choices[0].get('message', {})
            tool_calls = ai_message.get('tool_calls', [])
            
            if tool_calls:
                print(f"\nAI决定调用工具: {tool_calls[0].get('name')}")
                print(f"参数: {tool_calls[0].get('params')}")
                
                # 执行工具调用
                if tool_calls[0].get('name') == 'load_skill_content':
                    skill_name = tool_calls[0].get('params', {}).get('skill_name')
                    content_result = load_skill_content(skill_name)
                    print(f"\n工具执行结果: {content_result['status']}")
                    
                    if content_result['status'] == 'success':
                        # 添加工具执行结果到消息历史
                        messages.append({
                            "role": "assistant", 
                            "content": "",
                            "tool_calls": tool_calls
                        })
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_calls[0].get('id', '1'),
                            "content": json.dumps(content_result)
                        })
                        
                        # 第二次调用：让LLM根据技能内容生成通知
                        result2 = call_llm_with_tools(env_vars, messages)
                        if result2:
                            choices2 = result2.get('choices', [])
                            if choices2:
                                ai_message2 = choices2[0].get('message', {})
                                content2 = ai_message2.get('content', '')
                                print("\nAI生成的通知内容：")
                                print(content2)
                                
                                # 验证输出格式
                                if content2.startswith('XX部通知'):
                                    print("\n✅ 测试通过！输出以'XX部通知'开头")
                                else:
                                    print("\n❌ 测试失败！输出没有以'XX部通知'开头")
        else:
            content = ai_message.get('content', '')
            print(f"AI回复: {content}")
    
    # 测试2：用户提供部门"销售部"，要求撰写五一节放假通知
    print("\n\n【测试2】用户提供部门'销售部'，要求撰写五一节放假通知")
    print("-" * 60)
    print("用户输入：我是销售部的，请帮我撰写一份关于五一节放假的通知")
    
    messages2 = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "我是销售部的，请帮我撰写一份关于五一节放假的通知"}
    ]
    
    # 第一次调用：LLM决定是否调用工具
    result3 = call_llm_with_tools(env_vars, messages2)
    if result3:
        choices3 = result3.get('choices', [])
        if choices3:
            ai_message3 = choices3[0].get('message', {})
            tool_calls3 = ai_message3.get('tool_calls', [])
            
            if tool_calls3:
                print(f"\nAI决定调用工具: {tool_calls3[0].get('name')}")
                print(f"参数: {tool_calls3[0].get('params')}")
                
                # 执行工具调用
                if tool_calls3[0].get('name') == 'load_skill_content':
                    skill_name = tool_calls3[0].get('params', {}).get('skill_name')
                    content_result = load_skill_content(skill_name)
                    print(f"\n工具执行结果: {content_result['status']}")
                    
                    if content_result['status'] == 'success':
                        # 添加工具执行结果到消息历史
                        messages2.append({
                            "role": "assistant", 
                            "content": "",
                            "tool_calls": tool_calls3
                        })
                        messages2.append({
                            "role": "tool",
                            "tool_call_id": tool_calls3[0].get('id', '1'),
                            "content": json.dumps(content_result)
                        })
                        
                        # 第二次调用：让LLM根据技能内容生成通知
                        result4 = call_llm_with_tools(env_vars, messages2)
                        if result4:
                            choices4 = result4.get('choices', [])
                            if choices4:
                                ai_message4 = choices4[0].get('message', {})
                                content4 = ai_message4.get('content', '')
                                print("\nAI生成的通知内容：")
                                print(content4)
                                
                                # 验证输出格式
                                if content4.startswith('销售部通知'):
                                    print("\n✅ 测试通过！输出以'销售部通知'开头")
                                else:
                                    print("\n❌ 测试失败！输出没有以'销售部通知'开头")
        else:
            content = ai_message3.get('content', '')
            print(f"AI回复: {content}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_notice_skill()
