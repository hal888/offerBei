-- 更新用户表结构的MySQL语句
-- 适用于现有users表的结构更新

-- 1. 添加email字段：邮箱作为用户唯一标识
ALTER TABLE users
ADD COLUMN email VARCHAR(120) NOT NULL,
ADD CONSTRAINT uk_users_email UNIQUE (email);

-- 2. 添加password字段：加密后的密码
ALTER TABLE users
ADD COLUMN password VARCHAR(255) NOT NULL;

-- 3. 添加email_verified字段：邮箱是否已验证
ALTER TABLE users
ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE;

-- 4. 添加verification_code字段：邮箱验证码
ALTER TABLE users
ADD COLUMN verification_code VARCHAR(6) NULL;

-- 5. 添加verification_code_expiry字段：验证码过期时间
ALTER TABLE users
ADD COLUMN verification_code_expiry DATETIME NULL;

-- 6. 添加reset_password_token字段：密码重置令牌
ALTER TABLE users
ADD COLUMN reset_password_token VARCHAR(100) NULL;

-- 7. 添加reset_password_expiry字段：密码重置令牌过期时间
ALTER TABLE users
ADD COLUMN reset_password_expiry DATETIME NULL;

-- 8. 添加login_attempts字段：登录尝试次数
ALTER TABLE users
ADD COLUMN login_attempts INT NOT NULL DEFAULT 0;

-- 9. 添加locked_until字段：账号锁定时间
ALTER TABLE users
ADD COLUMN locked_until DATETIME NULL;

-- 10. 修改user_id字段：从NOT NULL改为NULL
-- 注意：如果原有数据中存在user_id为NULL的记录，需要先处理这些记录
ALTER TABLE users
MODIFY COLUMN user_id VARCHAR(36) NULL;

-- 11. 如果需要，可以添加创建时间和更新时间字段
-- 注意：如果表中已存在这些字段，可以跳过
-- ALTER TABLE users
-- ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- 12. 创建索引：优化查询性能
-- 为email字段创建索引，加速登录和注册时的查询
CREATE INDEX idx_users_email ON users(email);

-- 为reset_password_token字段创建索引，加速密码重置时的查询
CREATE INDEX idx_users_reset_password_token ON users(reset_password_token);

-- 13. 可选：如果需要，可以添加外键约束
-- 例如，如果有其他表引用users.id，可以添加外键约束
-- ALTER TABLE other_table
-- ADD CONSTRAINT fk_other_table_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;