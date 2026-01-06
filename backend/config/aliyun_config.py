# 阿里云ASR配置
# 更多配置说明请参考：https://help.aliyun.com/document_detail/155645.html

import os

ALIYUN_ASR_CONFIG = {
    "access_key_id": os.environ.get("ALIYUN_ACCESS_KEY_ID", ""),  # 阿里云访问密钥ID
    "access_key_secret": os.environ.get("ALIYUN_ACCESS_KEY_SECRET", ""),  # 阿里云访问密钥Secret
    "app_key": os.environ.get("ALIYUN_ASR_APP_KEY", ""),  # 阿里云智能语音服务AppKey
    "region_id": os.environ.get("ALIYUN_REGION_ID", "cn-shanghai"),  # 服务地域
    "format": os.environ.get("ALIYUN_ASR_FORMAT", "wav"),  # 音频格式，支持wav、opus、mp3等
    "sample_rate": int(os.environ.get("ALIYUN_ASR_SAMPLE_RATE", "16000")),  # 采样率，支持8000、16000等
    "enable_punctuation_prediction": os.environ.get("ALIYUN_ASR_ENABLE_PUNCTUATION", "True").lower() == "true",  # 是否开启标点预测
    "enable_inverse_text_normalization": os.environ.get("ALIYUN_ASR_ENABLE_ITN", "True").lower() == "true"  # 是否开启ITN
}

# 阿里云ASR服务URL
ALIYUN_ASR_URL = {
    "cn-shanghai": "https://nls-gateway-cn-shanghai.aliyuncs.com",
    "cn-beijing": "https://nls-gateway-cn-beijing.aliyuncs.com",
    "cn-hangzhou": "https://nls-gateway-cn-hangzhou.aliyuncs.com",
    "ap-southeast-1": "https://nls-gateway-ap-southeast-1.aliyuncs.com"
}
