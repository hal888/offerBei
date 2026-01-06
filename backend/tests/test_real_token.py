#!/usr/bin/env python3
"""
测试阿里云ASR真实Token生成

该脚本用于测试使用阿里云官方SDK生成真实Token的功能，
包括检查配置、初始化客户端、发送请求等步骤。
"""

import os
import sys
import json

import requests
import glob

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

from config import ALIYUN_ASR_CONFIG, ALIYUN_ASR_URL

def test_real_token_generation():
    """
    测试生成真实Token
    """
    print("=== 测试阿里云ASR真实Token生成 ===\n")
    
    try:
        # 检查配置
        print("检查阿里云ASR配置...")
        required_configs = ["access_key_id", "access_key_secret", "app_key", "region_id"]
        for config in required_configs:
            if not ALIYUN_ASR_CONFIG.get(config):
                print(f"✗ 缺少必要配置: {config}")
                return None
        print("✓ 配置检查通过")
        
        # 打印配置信息（隐藏敏感信息）
        print(f"配置信息:")
        print(f"  Region ID: {ALIYUN_ASR_CONFIG['region_id']}")
        print(f"  Access Key ID: {ALIYUN_ASR_CONFIG['access_key_id'][:10]}...")
        print(f"  Access Key Secret: {ALIYUN_ASR_CONFIG['access_key_secret'][:10]}...")
        print(f"  App Key: {ALIYUN_ASR_CONFIG['app_key']}")
        
        # 尝试导入阿里云SDK
        print("\n尝试导入阿里云SDK...")
        try:
            from aliyunsdkcore.client import AcsClient
            from aliyunsdknls_cloud_meta.request.v20180518.CreateTokenRequest import CreateTokenRequest
            print("✓ 阿里云SDK导入成功")
        except ImportError as e:
            print(f"✗ 阿里云SDK导入失败: {e}")
            print("请确保已安装aliyun-python-sdk-core-v3和aliyun-python-sdk-nls-cloud-meta包")
            print("安装命令: pip install aliyun-python-sdk-core-v3 aliyun-python-sdk-nls-cloud-meta")
            return None
        
        # 尝试初始化AcsClient
        print("\n尝试初始化AcsClient...")
        try:
            client = AcsClient(
                ALIYUN_ASR_CONFIG['access_key_id'],
                ALIYUN_ASR_CONFIG['access_key_secret'],
                ALIYUN_ASR_CONFIG['region_id']
            )
            print("✓ AcsClient初始化成功")
        except Exception as e:
            print(f"✗ AcsClient初始化失败: {e}")
            return None
        
        # 尝试创建请求
        print("\n尝试创建CreateTokenRequest...")
        try:
            request = CreateTokenRequest()
            request.set_accept_format('json')
            # 为请求显式设置端点，解决端点解析错误
            request.set_endpoint(f"nls-meta.{ALIYUN_ASR_CONFIG['region_id']}.aliyuncs.com")
            print("✓ CreateTokenRequest创建成功")
        except Exception as e:
            print(f"✗ CreateTokenRequest创建失败: {e}")
            return None
        
        # 尝试发送请求
        print("\n尝试发送CreateToken请求...")
        try:
            response = client.do_action_with_exception(request)
            print("✓ 请求发送成功")
            
            # 解析响应
            print("解析响应...")
            result = json.loads(response.decode('utf-8'))
            print(f"响应结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 根据实际响应格式判断，阿里云ASR API返回的是Token字段和ErrMsg字段
            if "Token" in result and result.get("ErrMsg") == "":
                token = result["Token"]["Id"]
                expire_time = result["Token"]["ExpireTime"]
                print(f"\n✓ 真实Token生成成功!")
                print(f"Token: {token}")
                print(f"过期时间: {expire_time}")
                print(f"剩余时间: {expire_time - int(time.time())}秒")
                return token
            else:
                error_msg = result.get("ErrMsg", result.get("Message", "生成Token失败"))
                print(f"\n✗ Token生成失败: {error_msg}")
                print(f"错误代码: {result.get('Code')}")
                return None
                
        except Exception as e:
            print(f"\n✗ 请求发送失败: {e}")
            print(f"错误类型: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return None
            
    except Exception as e:
        print(f"\n✗ 测试过程中发生未知错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_asr_transcription(token):
    """
    测试ASR语音转文字
    """
    print("\n=== 测试阿里云ASR语音转文字 ===")
    
    # 查找测试音频文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(script_dir, "temp_audio")
    audio_files = glob.glob(os.path.join(audio_dir, "*.wav"))
    
    if not audio_files:
        print("⚠ 未找到测试音频文件，跳过ASR测试")
        print(f"请在 {audio_dir} 目录下放置 .wav 文件")
        return False
        
    audio_file = audio_files[0]
    print(f"使用音频文件: {audio_file}")
    
    try:
        # 读取音频数据
        with open(audio_file, "rb") as f:
            audio_data = f.read()
        print(f"音频大小: {len(audio_data)} bytes")
        
        # 构建请求URL
        region_id = ALIYUN_ASR_CONFIG['region_id']
        service_url = ALIYUN_ASR_URL.get(region_id, ALIYUN_ASR_URL["cn-shanghai"])
        
        params = {
            "appkey": ALIYUN_ASR_CONFIG['app_key'],
            "format": "wav",
            "sample_rate": 16000,
            "enable_punctuation_prediction": "true",
            "enable_inverse_text_normalization": "true"
        }
        
        url = f"{service_url}/stream/v1/asr?{requests.compat.urlencode(params)}"
        print(f"请求URL: {url}")
        
        # 构建请求头
        headers = {
            "Content-Type": "application/octet-stream",
            "X-NLS-Token": token,
            "Authorization": f"Bearer {token}",
            "X-NLS-AppKey": ALIYUN_ASR_CONFIG['app_key']
        }
        
        # 发送请求
        print("发送ASR请求...")
        print(f"请求头: {headers}")
        response = requests.post(url, headers=headers, data=audio_data, timeout=30)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == 20000000:
                print(f"\n✓ 语音识别成功!")
                print(f"识别结果: {result.get('result')}")
                return True
            else:
                print(f"\n✗ 语音识别失败: {result.get('message')}")
                return False
        else:
            print(f"\n✗ 请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n✗ ASR测试发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    """
    运行测试
    """
    import time
    
    # 1. 测试Token生成
    token = test_real_token_generation()
    
    if token:
        # 2. 测试语音转文字
        asr_success = test_asr_transcription(token)
        
        if asr_success:
            print("\n=== 所有测试通过！ ===")
            sys.exit(0)
        else:
            print("\n=== Token生成成功，但ASR测试失败 ===")
            sys.exit(1)
    else:
        print("\n=== Token生成失败，跳过ASR测试 ===")
        sys.exit(1)
