#!/usr/bin/env python3
"""
测试阿里云ASR服务客户端
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

from app.services.aliyun_asr_service import AliyunASRService

def test_aliyun_asr_service():
    """
    测试阿里云ASR服务客户端
    """
    print("正在测试阿里云ASR服务客户端...")
    
    try:
        # 初始化服务
        asr_service = AliyunASRService()
        print("✓ 阿里云ASR服务客户端初始化成功")
        
        # 测试Token生成
        print("正在测试Token生成...")
        token, expire_time = asr_service._generate_token()
        print(f"✓ Token生成成功: {token[:20]}...")
        print(f"✓ Token过期时间: {expire_time}")
        
        print("\n所有测试通过！阿里云ASR服务客户端工作正常。")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_aliyun_asr_service()
    sys.exit(0 if success else 1)
