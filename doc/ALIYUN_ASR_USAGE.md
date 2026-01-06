# 阿里云ASR语音转文字服务使用文档

## 1. 功能概述

本文档介绍如何在模拟面试系统中配置和使用阿里云智能语音识别（ASR）服务。通过本服务，您可以将语音转换为文字，支持与现有Faster Whisper方案进行效果对比测试。

## 2. 准备工作

### 2.1 开通阿里云智能语音服务

1. 登录阿里云控制台：https://console.aliyun.com/
2. 搜索并进入"智能语音交互"服务
3. 点击"开通服务"，选择合适的计费方式
4. 创建项目，获取AppKey

### 2.2 获取阿里云AccessKey

1. 进入阿里云AccessKey管理页面：https://ram.console.aliyun.com/manage/ak
2. 创建或选择已有的AccessKey
3. 保存AccessKey ID和AccessKey Secret

## 3. 配置说明

### 3.1 配置文件方式

编辑`backend/config/aliyun_config.py`文件，填入以下配置：

```python
ALIYUN_ASR_CONFIG = {
    "access_key_id": "您的AccessKey ID",
    "access_key_secret": "您的AccessKey Secret",
    "app_key": "您的AppKey",
    "region_id": "cn-shanghai",  # 服务地域，可选：cn-shanghai, cn-beijing, cn-hangzhou, ap-southeast-1
    "format": "wav",  # 音频格式，支持：wav, opus, mp3等
    "sample_rate": 16000,  # 采样率，支持：8000, 16000等
    "enable_punctuation_prediction": True,  # 是否开启标点预测
    "enable_inverse_text_normalization": True  # 是否开启ITN（数字转换）
}
```

### 3.2 环境变量方式

您也可以通过环境变量配置阿里云ASR服务：

```bash
# Linux/Mac
set ALIYUN_ACCESS_KEY_ID=您的AccessKey ID
set ALIYUN_ACCESS_KEY_SECRET=您的AccessKey Secret
set ALIYUN_ASR_APP_KEY=您的AppKey
set ALIYUN_REGION_ID=cn-shanghai
set ALIYUN_ASR_FORMAT=wav
set ALIYUN_ASR_SAMPLE_RATE=16000
set ALIYUN_ASR_ENABLE_PUNCTUATION=True
set ALIYUN_ASR_ENABLE_ITN=True

# Windows
set ALIYUN_ACCESS_KEY_ID=您的AccessKey ID
set ALIYUN_ACCESS_KEY_SECRET=您的AccessKey Secret
set ALIYUN_ASR_APP_KEY=您的AppKey
set ALIYUN_REGION_ID=cn-shanghai
set ALIYUN_ASR_FORMAT=wav
set ALIYUN_ASR_SAMPLE_RATE=16000
set ALIYUN_ASR_ENABLE_PUNCTUATION=True
set ALIYUN_ASR_ENABLE_ITN=True
```

## 4. API调用方式

### 4.1 语音回答API

#### 请求地址
`POST /api/mock-interview/voice-answer`

#### 请求参数
| 参数名 | 类型 | 说明 | 可选值 | 默认值 |
|--------|------|------|--------|--------|
| interviewId | string | 面试ID | - | - |
| questionId | int | 问题ID | - | - |
| engine | string | 语音识别引擎 | whisper, aliyun | whisper |
| audio | file | 音频文件 | - | - |

#### 请求示例

```bash
# 使用curl调用（Faster Whisper）
curl -X POST "http://localhost:5000/api/mock-interview/voice-answer" \
  -F "interviewId=interview_12345678" \
  -F "questionId=1" \
  -F "engine=whisper" \
  -F "audio=@test_audio.wav"

# 使用curl调用（阿里云ASR）
curl -X POST "http://localhost:5000/api/mock-interview/voice-answer" \
  -F "interviewId=interview_12345678" \
  -F "questionId=1" \
  -F "engine=aliyun" \
  -F "audio=@test_audio.wav"
```

### 4.2 实时语音API

#### 请求地址
`POST /api/mock-interview/realtime-voice`

#### 请求参数
| 参数名 | 类型 | 说明 | 可选值 | 默认值 |
|--------|------|------|--------|--------|
| interviewId | string | 面试ID | - | - |
| questionId | int | 问题ID | - | - |
| chunkIndex | int | 音频分片索引 | - | 0 |
| engine | string | 语音识别引擎 | whisper, aliyun | whisper |
| audio | file | 音频文件 | - | - |

#### 请求示例

```bash
# 使用curl调用（阿里云ASR）
curl -X POST "http://localhost:5000/api/mock-interview/realtime-voice" \
  -F "interviewId=interview_12345678" \
  -F "questionId=1" \
  -F "chunkIndex=0" \
  -F "engine=aliyun" \
  -F "audio=@chunk_0.wav"
```

## 5. 对比测试方法

### 5.1 单一音频文件对比

1. 准备一个测试音频文件
2. 使用以下命令分别调用两种语音识别引擎
3. 对比识别结果的准确性

```bash
# 使用Faster Whisper
curl -X POST "http://localhost:5000/api/mock-interview/voice-answer" \
  -F "interviewId=test_123" \
  -F "questionId=1" \
  -F "engine=whisper" \
  -F "audio=@test_audio.wav" \
  > whisper_result.json

# 使用阿里云ASR
curl -X POST "http://localhost:5000/api/mock-interview/voice-answer" \
  -F "interviewId=test_123" \
  -F "questionId=1" \
  -F "engine=aliyun" \
  -F "audio=@test_audio.wav" \
  > aliyun_result.json

# 对比结果
diff whisper_result.json aliyun_result.json
```

### 5.2 批量对比测试

1. 准备多个测试音频文件
2. 编写脚本批量调用API
3. 统计识别准确率、响应时间等指标
4. 生成对比报告

## 6. 性能测试

### 6.1 响应时间测试

```bash
# 使用time命令测试响应时间
# Faster Whisper
time curl -s -X POST "http://localhost:5000/api/mock-interview/voice-answer" \
  -F "interviewId=test_123" \
  -F "questionId=1" \
  -F "engine=whisper" \
  -F "audio=@test_audio.wav" \
  > /dev/null

# 阿里云ASR
time curl -s -X POST "http://localhost:5000/api/mock-interview/voice-answer" \
  -F "interviewId=test_123" \
  -F "questionId=1" \
  -F "engine=aliyun" \
  -F "audio=@test_audio.wav" \
  > /dev/null
```

### 6.2 并发测试

使用ab工具进行并发测试：

```bash
# Faster Whisper
ab -n 100 -c 10 -p post_data.txt -T "multipart/form-data" http://localhost:5000/api/mock-interview/voice-answer

# 阿里云ASR
ab -n 100 -c 10 -p post_data_aliyun.txt -T "multipart/form-data" http://localhost:5000/api/mock-interview/voice-answer
```

## 7. 日志与监控

### 7.1 日志查看

```bash
# 查看后端日志
cat /home/alan/traeProject/ai_interview2/backend/server.log

# 查看API日志
grep "mock-interview" /home/alan/traeProject/ai_interview2/backend/server.log
```

### 7.2 监控指标

系统会记录以下监控指标：
- 语音识别引擎使用次数
- 识别成功率
- 平均响应时间
- 错误率

## 8. 错误处理

### 8.1 常见错误及解决方案

| 错误信息 | 可能原因 | 解决方案 |
|----------|----------|----------|
| 阿里云ASR配置不完整 | 缺少AccessKey或AppKey | 检查配置文件或环境变量 |
| 生成Token失败 | 网络问题或配置错误 | 检查网络连接和配置 |
| 语音识别失败 | 音频格式不支持或质量差 | 确保音频格式为WAV、MP3或OPUS，采样率为16000Hz |
| 阿里云ASR服务不可用 | 服务维护或配置错误 | 检查阿里云控制台服务状态 |

### 8.2 降级策略

当阿里云ASR服务不可用时，系统会自动降级使用Faster Whisper模型，确保服务可用性。

## 9. 扩展与自定义

### 9.1 添加新的语音识别引擎

1. 在`backend/app/services/`目录下创建新的服务实现
2. 修改`transcribe_audio`函数，添加新引擎的支持
3. 更新API参数验证

### 9.2 自定义识别参数

您可以在`aliyun_config.py`中调整以下参数：

```python
ALIYUN_ASR_CONFIG = {
    "format": "wav",  # 音频格式
    "sample_rate": 16000,  # 采样率
    "enable_punctuation_prediction": True,  # 标点预测
    "enable_inverse_text_normalization": True  # ITN数字转换
}
```

## 10. 最佳实践

### 10.1 音频格式建议

- 推荐使用WAV或OPUS格式
- 采样率建议为16000Hz
- 声道数建议为单声道
- 音频质量建议不低于128kbps

### 10.2 性能优化

- 对于实时语音场景，建议使用较短的音频分片（1-2秒）
- 对于长音频，建议使用语音回答API
- 合理设置并发数，避免超过阿里云API配额

## 11. 常见问题

### 11.1 如何查看阿里云API调用配额？

登录阿里云控制台，进入智能语音交互服务，查看"API调用统计"页面。

### 11.2 如何提高识别准确率？

- 确保音频质量良好，无明显噪音
- 使用合适的音频格式和采样率
- 避免语速过快或过慢
- 清晰发音，避免口音过重

### 11.3 如何切换语音识别引擎？

通过API请求中的`engine`参数切换，可选值为`whisper`或`aliyun`。

## 12. 联系方式

如果您在使用过程中遇到问题，请联系系统管理员或查看阿里云官方文档：

- 阿里云智能语音交互文档：https://help.aliyun.com/zh/isi/
- 阿里云ASR API参考：https://help.aliyun.com/zh/isi/developer-reference/api-overview-1

---

**更新日期**：2026-01-04
**版本**：1.0.0