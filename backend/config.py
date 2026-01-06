# 配置文件
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取项目根目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# DeepSeek API配置
DEEPSEEK_CONFIG = {
    "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
    "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
}

# 数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "ai_interview_db"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10"))
}

# SQLAlchemy配置
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = DB_CONFIG['pool_size']
SQLALCHEMY_MAX_OVERFLOW = DB_CONFIG['max_overflow']

# 简历保存路径配置
RESUME_CONFIG = {
    "base_path": os.getenv("RESUME_BASE_PATH", os.path.join(BASE_DIR, "resumes")),
    "original_path": os.getenv("RESUME_ORIGINAL_PATH", "original"),
    "optimized_path": os.getenv("RESUME_OPTIMIZED_PATH", "optimized")
}

# 邮件发送配置
MAIL_CONFIG = {
    "server": os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    "port": int(os.getenv("MAIL_PORT", "587")),
    "username": os.getenv("MAIL_USERNAME", ""),
    "password": os.getenv("MAIL_PASSWORD", ""),
    "use_tls": os.getenv("MAIL_USE_TLS", "True").lower() == "true",
    "use_ssl": os.getenv("MAIL_USE_SSL", "False").lower() == "true",
    "default_sender": os.getenv("MAIL_DEFAULT_SENDER", "")
}

# JWT配置
JWT_CONFIG = {
    "secret_key": os.getenv("JWT_SECRET_KEY", "default_secret_key_override_in_production"),
    "algorithm": os.getenv("JWT_ALGORITHM", "HS256"),
    "access_token_expiry": int(os.getenv("JWT_ACCESS_TOKEN_EXPIRY", "604800"))  # 7天
}

# 认证配置
AUTH_CONFIG = {
    "verification_code_expiry": int(os.getenv("VERIFICATION_CODE_EXPIRY", "900")),  # 15分钟
    "reset_password_expiry": int(os.getenv("RESET_PASSWORD_EXPIRY", "86400")),  # 24小时
    "max_login_attempts": int(os.getenv("MAX_LOGIN_ATTEMPTS", "5")),  # 最大登录尝试次数
    "lock_duration": int(os.getenv("LOCK_DURATION", "300"))  # 账号锁定时间（秒）
}

# 阿里云ASR配置
ALIYUN_ASR_CONFIG = {
    "access_key_id": os.getenv("ALIYUN_ACCESS_KEY_ID", ""),
    "access_key_secret": os.getenv("ALIYUN_ACCESS_KEY_SECRET", ""),
    "app_key": os.getenv("ALIYUN_ASR_APP_KEY", ""),
    "region_id": os.getenv("ALIYUN_REGION_ID", "cn-shanghai"),
    "format": os.getenv("ALIYUN_ASR_FORMAT", "wav"),
    "sample_rate": int(os.getenv("ALIYUN_ASR_SAMPLE_RATE", "16000")),
    "enable_punctuation_prediction": os.getenv("ALIYUN_ASR_ENABLE_PUNCTUATION", "True").lower() == "true",
    "enable_inverse_text_normalization": os.getenv("ALIYUN_ASR_ENABLE_ITN", "True").lower() == "true"
}

# 阿里云ASR服务URL
ALIYUN_ASR_URL = {
    "cn-shanghai": "https://nls-gateway-cn-shanghai.aliyuncs.com",
    "cn-beijing": "https://nls-gateway-cn-beijing.aliyuncs.com",
    "cn-hangzhou": "https://nls-gateway-cn-hangzhou.aliyuncs.com",
    "ap-southeast-1": "https://nls-gateway-ap-southeast-1.aliyuncs.com"
}