#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试：验证自我介绍API端到端多语言工作流程
"""

import sys
sys.path.insert(0, '/home/alan/Antigravity/offerBei/backend')

# 模拟Flask请求
from flask import Flask
from app.routes.self_intro import get_localized_version_style

def test_localization_function():
    """测试locale转换函数"""
    
    print("=" * 60)
    print("测试 get_localized_version_style 函数")
    print("=" * 60)
    
    # 测试中文locale
    print("\n[测试1] 中文locale - 保持原样")
    version_zh, style_zh = get_localized_version_style('30秒电梯演讲版', '正式', 'zh')
    print(f"  输入: version='30秒电梯演讲版', style='正式', locale='zh'")
    print(f"  输出: version='{version_zh}', style='{style_zh}'")
    assert version_zh == '30秒电梯演讲版', "中文version应保持不变"
    assert style_zh == '正式', "中文style应保持不变"
    print("  ✓ 通过")
    
    # 测试英文locale
    print("\n[测试2] 英文locale - 转换为英文")
    version_en, style_en = get_localized_version_style('30秒电梯演讲版', '正式', 'en')
    print(f"  输入: version='30秒电梯演讲版', style='正式', locale='en'")
    print(f"  输出: version='{version_en}', style='{style_en}'")
    assert version_en == '30s Elevator Pitch', f"英文version错误: {version_en}"
    assert style_en == 'Formal', f"英文style错误: {style_en}"
    print("  ✓ 通过")
    
    # 测试其他组合
    print("\n[测试3] 其他版本/风格组合")
    test_cases = [
        ('3分钟版', '活泼', 'en', '3 Minute Version', 'Casual'),
        ('1分钟版', '专业', 'en', '1 Minute Version', 'Academic'),
        ('3分钟版', '亲切', 'zh', '3分钟版', '亲切'),
    ]
    
    for version_in, style_in, locale, expected_v, expected_s in test_cases:
        v_out, s_out = get_localized_version_style(version_in, style_in, locale)
        print(f"  {version_in} + {style_in} ({locale}) → {v_out} + {s_out}")
        assert v_out == expected_v and s_out == expected_s, f"转换错误: {v_out}, {s_out}"
    print("  ✓ 所有组合通过")
    
    print("\n" + "=" * 60)
    print("✓ 所有测试通过！locale转换函数工作正常")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_localization_function()
    sys.exit(0 if success else 1)
