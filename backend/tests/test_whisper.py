#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Faster Whisper 模型测试脚本
用于验证Faster Whisper模型是否能正常工作
"""

import os
import sys

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_faster_whisper_import():
    """测试Faster Whisper模块是否能正常导入"""
    print("测试Faster Whisper模块导入...")
    try:
        from faster_whisper import WhisperModel
        print("✓ Faster Whisper模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ Faster Whisper模块导入失败: {e}")
        return False

def test_model_initialization():
    """测试Faster Whisper模型是否能正常初始化"""
    print("\n测试Faster Whisper模型初始化...")
    try:
        from faster_whisper import WhisperModel
        
        # 模型列表，从大到小尝试
        # model_sizes = ["small"]
        model_size = os.path.expanduser("~/.cache/huggingface/hub/models--guillaumekln--faster-whisper-small/snapshots/9193eb88f0308584598e31c92ac6833e08f72599")

        try:
            # 尝试初始化模型
            print(f"正在加载模型: {model_size}...")
            model = WhisperModel(model_size, device="cpu", compute_type="int8")
            print(f"✓ Faster Whisper模型初始化成功: {model_size}")
            return model
        except Exception as e:
            print(f"✗ Faster Whisper {model_size} 模型初始化失败: {e}")
    
        # 所有模型都失败
        print("✗ 所有Faster Whisper模型初始化失败")
        return None
    except Exception as e:
        print(f"✗ Faster Whisper模型初始化失败: {e}")
        return None

def test_transcription(model):
    """测试Faster Whisper模型的转录功能"""
    if not model:
        print("\n✗ 模型未初始化，跳过转录测试")
        return False
    
    print("\n测试Faster Whisper模型转录功能...")
    
    # 检查是否存在测试音频文件
    test_audio_path = "test.mp3"
    if not os.path.exists(test_audio_path):
        print(f"✗ 测试音频文件 {test_audio_path} 不存在，创建一个简单的测试音频")
        
        # 创建一个简单的测试音频（这里只是示例，实际可能需要生成一个真实的音频文件）
        try:
            import wave
            import struct
            
            # 创建一个1秒的静音WAV文件
            sample_rate = 16000
            duration = 1  # 1秒
            num_samples = sample_rate * duration
            
            with wave.open("test.wav", 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                
                # 写入静音数据
                for i in range(num_samples):
                    wav_file.writeframes(struct.pack('<h', 0))
            
            test_audio_path = "test.wav"
            print(f"✓ 创建了测试音频文件 {test_audio_path}")
        except Exception as e:
            print(f"✗ 创建测试音频失败: {e}")
            return False
    
    try:
        # 使用模型进行转录
        print(f"正在转录音频文件: {test_audio_path}")
        segments, info = model.transcribe(test_audio_path, beam_size=5, language="zh")
        
        # 打印结果
        print(f"✓ 转录成功！")
        print(f"  检测到语言: {info.language} (概率: {info.language_probability:.2f})")
        
        transcribed_text = ""
        for segment in segments:
            transcribed_text += segment.text
            print(f"  [{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        
        print(f"✓ 完整转录结果: {transcribed_text}")
        return True
    except Exception as e:
        print(f"✗ 转录失败: {e}")
        return False

def test_flask_app_integration():
    """测试Flask应用中的Faster Whisper集成"""
    print("\n测试Flask应用中的Faster Whisper集成...")
    
    try:
        # 导入Flask应用和模型
        from backend.app import app, whisper_model
        
        print("✓ Flask应用导入成功")
        print(f"✓ Faster Whisper模型状态: {'已加载' if whisper_model else '未加载'}")
        
        return True
    except Exception as e:
        print(f"✗ Flask应用集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("Faster Whisper 模型测试脚本")
    print("=" * 60)
    
    # 运行所有测试
    results = []
    
    results.append(('模块导入', test_faster_whisper_import()))
    model = test_model_initialization()
    results.append(('模型初始化', model is not None))
    results.append(('转录功能', test_transcription(model)))
    results.append(('Flask集成', test_flask_app_integration()))
    
    # 打印测试结果汇总
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 成功" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    print("\n" + "=" * 60)
    print(f"总体结果: {passed}/{total} 测试通过")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 所有测试通过！Faster Whisper模型可以正常使用。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查相关配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
