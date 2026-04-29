# -*- coding: utf-8 -*-
import os
import sys
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from tool_client import list_available_skills, load_skill_content

def generate_notice(department, content):
    """
    根据部门和内容生成通知
    """
    # 加载通知撰写技能
    skill_result = load_skill_content("通知撰写")
    
    if skill_result["status"] == "success":
        skill_content = skill_result["data"]
        
        # 根据技能要求生成通知标题
        if department and department.strip():
            title = "{0}通知".format(department.strip())
        else:
            title = "XX部通知"
        
        # 生成通知内容
        notice = """{0}

{1}

特此通知。

【发布部门】{2}
【发布日期】2025年4月29日""".format(title, content, department.strip() if department else 'XX部')
        
        return notice
    else:
        return "无法加载通知撰写技能: {0}".format(skill_result['message'])

def test_notice_skill_simple():
    """
    简单测试通知撰写技能
    """
    print("=" * 60)
    print("测试通知撰写技能")
    print("=" * 60)
    
    # 首先验证技能列表
    print("\n【步骤1】验证技能列表")
    print("-" * 60)
    skills_result = list_available_skills()
    
    if skills_result["status"] == "success":
        skills = skills_result["data"]
        notice_skill = None
        
        for skill in skills:
            if skill["name"] == "通知撰写":
                notice_skill = skill
                break
        
        if notice_skill:
            print("找到'通知撰写'技能")
            print("   名称: {0}".format(notice_skill['name']))
            print("   描述: {0}".format(notice_skill['description']))
            print("   [测试通过]")
        else:
            print("未找到'通知撰写'技能")
            print("   [测试失败]")
            return
    else:
        print("读取技能列表失败: {0}".format(skills_result['message']))
        print("   [测试失败]")
        return
    
    # 验证技能内容加载
    print("\n【步骤2】验证技能内容加载")
    print("-" * 60)
    skill_content_result = load_skill_content("通知撰写")
    
    if skill_content_result["status"] == "success":
        content = skill_content_result["data"]
        print("成功加载技能内容（前150字符）:")
        if len(content) > 150:
            print(content[:150] + "...")
        else:
            print(content)
        print("[测试通过]")
    else:
        print("加载技能内容失败: {0}".format(skill_content_result['message']))
        print("[测试失败]")
        return
    
    # 测试1：用户不提供部门
    print("\n【测试1】用户不提供部门，撰写五一节放假通知")
    print("-" * 60)
    notice1 = generate_notice("", """根据国务院办公厅关于2025年劳动节假期安排的通知，结合公司实际情况，现将五一劳动节放假安排通知如下：

一、放假时间：2025年5月1日（星期四）至5月5日（星期一）放假调休，共5天。4月28日（星期日）、5月11日（星期六）上班。

二、请各部门做好放假前的安全检查工作，关闭不必要的电源设备，确保办公区域安全。

三、放假期间如有紧急事务，请联系各部门值班人员。""")
    
    print(notice1)
    
    if notice1.startswith("XX部通知"):
        print("\n[测试1通过] 通知以'XX部通知'开头")
    else:
        print("\n[测试1失败] 通知没有以'XX部通知'开头")
    
    # 测试2：用户提供部门"销售部"
    print("\n【测试2】用户提供部门'销售部'，撰写五一节放假通知")
    print("-" * 60)
    notice2 = generate_notice("销售部", """根据国务院办公厅关于2025年劳动节假期安排的通知，结合公司实际情况，现将五一劳动节放假安排通知如下：

一、放假时间：2025年5月1日（星期四）至5月5日（星期一）放假调休，共5天。4月28日（星期日）、5月11日（星期六）上班。

二、请各部门做好放假前的安全检查工作，关闭不必要的电源设备，确保办公区域安全。

三、销售部员工请在放假前完成手头订单的跟进工作，确保客户服务不受影响。

四、放假期间如有紧急事务，请联系部门值班人员。""")
    
    print(notice2)
    
    if notice2.startswith("销售部通知"):
        print("\n[测试2通过] 通知以'销售部通知'开头")
    else:
        print("\n[测试2失败] 通知没有以'销售部通知'开头")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_notice_skill_simple()
