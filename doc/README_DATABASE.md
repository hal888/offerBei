# 面试宝典系统 - 数据库配置说明

## 1. MySQL数据库安装与配置

### 1.1 安装MySQL

#### Ubuntu/Debian系统
```bash
# 更新软件包列表
sudo apt update

# 安装MySQL服务器和客户端
sudo apt install -y mysql-server mysql-client

# 启动MySQL服务
sudo systemctl start mysql

# 设置MySQL开机自启
sudo systemctl enable mysql

# 运行安全配置向导
sudo mysql_secure_installation
```

#### CentOS/RHEL系统
```bash
# 安装MySQL服务器和客户端
sudo yum install -y mysql-server mysql-client

# 启动MySQL服务
sudo systemctl start mysqld

# 设置MySQL开机自启
sudo systemctl enable mysqld

# 运行安全配置向导
sudo mysql_secure_installation
```

### 1.2 创建数据库和用户

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE ai_interview_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户并授权
CREATE USER 'ai_interview_user'@'localhost' IDENTIFIED BY 'ai_interview_password';
GRANT ALL PRIVILEGES ON ai_interview_db.* TO 'ai_interview_user'@'localhost';
FLUSH PRIVILEGES;

# 退出MySQL
EXIT;
```

### 1.3 修改配置文件

编辑 `config.py` 文件，更新数据库配置：

```python
# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "ai_interview_user",  # 替换为实际用户名
    "password": "ai_interview_password",  # 替换为实际密码
    "database": "ai_interview_db",
    "charset": "utf8mb4",
    "pool_size": 5,
    "max_overflow": 10
}
```

## 2. 初始化数据库

### 2.1 运行初始化脚本

```bash
cd /home/alan/traeProject/ai_interview2/backend
python3 init_db.py
```

### 2.2 验证数据库初始化

```bash
# 登录MySQL
mysql -u ai_interview_user -p ai_interview_db

# 查看所有表
SHOW TABLES;

# 退出MySQL
EXIT;
```

## 3. 数据库表结构

系统包含以下表：

### 3.1 users表
- 存储用户信息
- 字段：id, user_id, created_at, updated_at

### 3.2 resumes表
- 存储简历数据
- 字段：id, resume_id, user_id, original_content, optimized_content, score, diagnosis, keywords, star_rewrite, created_at, updated_at

### 3.3 self_intros表
- 存储自我介绍数据
- 字段：id, user_id, resume_id, self_intro_type, content, created_at, updated_at

### 3.4 question_banks表
- 存储智能题库数据
- 字段：id, user_id, resume_id, questions, created_at, updated_at

### 3.5 mock_interviews表
- 存储模拟面试数据
- 字段：id, user_id, resume_id, interview_id, style, mode, duration, questions, answers, feedbacks, report, is_completed, created_at, updated_at

### 3.6 interview_strategies表
- 存储面试策略数据
- 字段：id, user_id, resume_id, background_info, directions, analysis_result, company_info, question_types, generated_questions, created_at, updated_at

## 4. 备选方案：使用SQLite

如果MySQL不可用，可以使用SQLite作为备选：

### 4.1 修改配置文件

编辑 `config.py` 文件，替换数据库配置：

```python
# 导入os
import os

# 获取项目根目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLite配置
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'ai_interview.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 4.2 运行初始化脚本

```bash
cd /home/alan/traeProject/ai_interview2/backend
python3 init_db.py
```

## 5. 启动应用

### 5.1 启动后端服务

```bash
cd /home/alan/traeProject/ai_interview2/backend
python3 run.py
```

### 5.2 启动前端服务

```bash
cd /home/alan/traeProject/ai_interview2
npm run dev
```

## 6. 功能说明

- 用户首次访问页面时，系统会生成唯一的user_id并保存到localStorage
- 生成的数据会保存到数据库
- 再次访问页面时，系统会自动从数据库查询并显示之前生成的数据
- 支持多用户隔离，每个用户只能访问自己的数据

## 7. 数据流程图

```
用户访问页面 → 检查localStorage中的user_id → 无user_id则生成并保存 → 查询数据库获取已生成数据 → 显示数据或生成新数据 → 保存新数据到数据库
```

## 8. 注意事项

- 确保数据库服务正常运行
- 定期备份数据库
- 生产环境中使用强密码
- 定期清理过期数据
- 监控数据库性能
