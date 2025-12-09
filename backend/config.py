# 配置文件
import os

# 获取项目根目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# DeepSeek API配置
DEEPSEEK_CONFIG = {
    "api_key": "",  # 这里需要替换为实际的DeepSeek API密钥
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat"
}

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",  # 数据库用户名
    "password": "123456",  # 数据库密码
    "database": "ai_interview_db",  # 数据库名称
    "charset": "utf8mb4",
    "pool_size": 5,
    "max_overflow": 10
}

# SQLAlchemy配置
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = DB_CONFIG['pool_size']
SQLALCHEMY_MAX_OVERFLOW = DB_CONFIG['max_overflow']

# 简历保存路径配置
RESUME_CONFIG = {
    "base_path": os.path.join(BASE_DIR, "resumes"),  # 简历保存的基础路径（绝对路径）
    "original_path": "original",  # 原始简历保存路径（相对于base_path）
    "optimized_path": "optimized"  # 优化后简历保存路径（相对于base_path）
}
