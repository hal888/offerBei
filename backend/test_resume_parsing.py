#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证简历分析JSON解析修复
使用23.pdf测试DeepSeek API返回的JSON并验证解析逻辑
"""

import sys
import os
sys.path.insert(0, '/home/alan/Antigravity/offerBei/backend')

from app.services.file_service import read_file_content
from app.services.deepseek_service import analyze_resume
from app.utils.json_parser import parse_resume_result
import json

def test_resume_analysis():
    """测试简历分析流程"""
    pdf_path = '/home/alan/Antigravity/offerBei/doc/23.pdf'
    
    print("=" * 60)
    print("测试简历分析JSON解析")
    print("=" * 60)
    
    # 1. 读取PDF内容
    print("\n[步骤1] 读取PDF文件...")
    try:
        resume_content = read_file_content(pdf_path, 'pdf')
        print(f"✓ PDF内容读取成功，长度: {len(resume_content)} 字符")
        print(f"  前100字符: {resume_content[:100]}...")
    except Exception as e:
        print(f"✗ PDF读取失败: {e}")
        return False
    
    # 2. 调用DeepSeek API
    print("\n[步骤2] 调用DeepSeek API分析...")
    try:
        # 使用英文locale测试（因为错误日志显示是英文输出）
        api_result = analyze_resume(resume_content, locale='en')
        print(f"✓ API调用成功")
        print(f"  返回内容长度: {len(api_result)} 字符")
        
        # 保存原始响应用于调试
        with open('/tmp/deepseek_raw_response.txt', 'w', encoding='utf-8') as f:
            f.write(api_result)
        print(f"  原始响应已保存到: /tmp/deepseek_raw_response.txt")
        
        # 显示前500字符
        print(f"\n  响应前500字符:")
        print("  " + "-" * 56)
        print("  " + api_result[:500])
        print("  " + "-" * 56)
        
    except Exception as e:
        print(f"✗ API调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 3. 解析JSON
    print("\n[步骤3] 解析JSON响应...")
    try:
        parsed_result = parse_resume_result(api_result)
        print(f"✓ JSON解析成功！")
        print(f"\n解析结果:")
        print(f"  - 评分: {parsed_result['score']}")
        print(f"  - 诊断意见数: {len(parsed_result['diagnosis'])}")
        print(f"  - 关键词数: {len(parsed_result['keywords'])}")
        print(f"  - STAR重写数: {len(parsed_result['starRewrite'])}")
        print(f"  - 优化简历长度: {len(parsed_result['optimizedResume'])} 字符")
        
        # 显示部分诊断
        if parsed_result['diagnosis']:
            print(f"\n  诊断意见示例:")
            for i, diag in enumerate(parsed_result['diagnosis'][:2], 1):
                print(f"    {i}. [{diag['type']}] {diag['title']}")
                print(f"       {diag['description'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ JSON解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_resume_analysis()
    print("\n" + "=" * 60)
    if success:
        print("✓ 测试通过！JSON解析正常工作")
    else:
        print("✗ 测试失败！需要修复JSON解析逻辑")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
