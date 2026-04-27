import os
import sys
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from tool_client import list_available_skills, load_skill_content

def test_skills():
    """
    测试技能管理功能
    """
    print("=" * 60)
    print("测试技能管理功能")
    print("=" * 60)
    
    # 测试1：读取技能列表
    print("\n【测试1】读取技能列表")
    print("-" * 60)
    skills_result = list_available_skills()
    
    if skills_result["status"] == "success":
        skills = skills_result["data"]
        print(f"成功读取到 {len(skills)} 个技能：")
        print(json.dumps({"skills": skills}, ensure_ascii=False, indent=2))
    else:
        print(f"读取失败: {skills_result['message']}")
    
    # 测试2：加载技能内容
    print("\n【测试2】加载技能内容")
    print("-" * 60)
    if skills_result["status"] == "success" and skills:
        for skill in skills:
            skill_name = skill["name"]
            print(f"\n加载技能: {skill_name}")
            print(f"描述: {skill['description']}")
            
            content_result = load_skill_content(skill_name)
            if content_result["status"] == "success":
                content = content_result["data"]
                print(f"\n技能内容预览（前200字符）:")
                print(content[:200] + "..." if len(content) > 200 else content)
            else:
                print(f"加载失败: {content_result['message']}")
    else:
        print("没有可用的技能进行测试")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_skills()
