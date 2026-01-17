#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证自我介绍多语言生成
"""

import sys
sys.path.insert(0, '/home/alan/Antigravity/offerBei/backend')

from app.services.deepseek_service import generate_self_intro

def test_self_intro_multilingual():
    """测试自我介绍多语言生成"""
    
    resume_content = """
    # 张三 - Software Engineer
    
    ## Work Experience
    - 2020-Present: Software Engineer at TechCorp
    - Developed microservices using Python and Java
    - Led team of 3 developers
    
    ## Skills
    Python, Java, React, AWS, Docker
    """
    
    print("=" * 60)
    print("测试自我介绍多语言生成")
    print("=" * 60)
    
    # 测试中文
    print("\n[测试1] 中文 - 30秒电梯演讲版 - 正式风格")
    print("-" * 60)
    try:
        intro_zh = generate_self_intro(
            resume_content=resume_content,
            version='30秒电梯演讲版',
            style='正式',
            locale='zh'
        )
        print(f"✓ 中文自我介绍生成成功")
        print(f"长度: {len(intro_zh)} 字符")
        print(f"内容预览:\n{intro_zh[:200]}...")
    except Exception as e:
        print(f"✗ 中文生成失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试英文
    print("\n[测试2] 英文 - 30s Elevator - Formal风格")
    print("-" * 60)
    try:
        intro_en = generate_self_intro(
            resume_content=resume_content,
            version='30s Elevator',
            style='Formal',
            locale='en'
        )
        print(f"✓ 英文自我介绍生成成功")
        print(f"长度: {len(intro_en)} 字符")
        print(f"内容预览:\n{intro_en[:200]}...")
        
        # 验证是英文
        if any(word in intro_en.lower() for word in ['hello', 'hi', 'good', 'my name', 'i am', 'software engineer']):
            print("✓ 确认内容为英文")
        else:
            print("⚠ 警告：内容可能不是英文")
            
    except Exception as e:
        print(f"✗ 英文生成失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_self_intro_multilingual()
