from flask import Blueprint, request, jsonify
from flask_mail import Message
from .. import app, mail
from ..models import db, User
from ..utils.jwt_utils import JWTUtil
from config import AUTH_CONFIG
import bcrypt
import random
import string
import datetime
from email_validator import validate_email, EmailNotValidError

# 创建蓝图
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 生成6位数字验证码
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# 发送邮箱验证码
def send_verification_email(email, code):
    try:
        msg = Message('Offer贝 - 邮箱验证码', recipients=[email])
        msg.body = f'您的邮箱验证码是：{code}，有效期为15分钟。请勿将验证码泄露给他人。'
        mail.send(msg)
        return True
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        return False

# 发送密码重置邮件
def send_reset_password_email(email, reset_link):
    try:
        msg = Message('Offer贝 - 密码重置链接', recipients=[email])
        msg.body = f'您请求重置密码，点击以下链接重置密码：{reset_link}\n\n该链接有效期为24小时，请及时使用。如果不是您本人操作，请忽略此邮件。'
        mail.send(msg)
        return True
    except Exception as e:
        print(f"发送密码重置邮件失败: {str(e)}")
        return False

# 验证邮箱格式
def validate_email_format(email):
    try:
        v = validate_email(email)
        return True, v.email
    except EmailNotValidError as e:
        return False, str(e)

@bp.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    """发送邮箱验证码API"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "邮箱不能为空"}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": f"邮箱格式无效：{message}"}), 400
    
    # 生成验证码
    code = generate_verification_code()
    
    # 设置验证码过期时间
    expiry = datetime.datetime.now() + datetime.timedelta(seconds=AUTH_CONFIG['verification_code_expiry'])
    
    # 保存验证码到数据库（如果用户已存在则更新，否则创建临时记录）
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, password='temp_password')
        db.session.add(user)
    
    user.verification_code = code
    user.verification_code_expiry = expiry
    db.session.commit()
    
    # 发送验证码邮件
    success = send_verification_email(email, code)
    if success:
        return jsonify({"message": "验证码已发送到您的邮箱"}), 200
    else:
        return jsonify({"error": "发送验证码失败，请检查邮箱配置或稍后重试"}), 500

@bp.route('/register', methods=['POST'])
def register():
    """用户注册API"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    code = data.get('verificationCode')
    
    if not email or not password or not code:
        return jsonify({"error": "邮箱、密码和验证码不能为空"}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": f"邮箱格式无效：{message}"}), 400
    
    # 检查密码长度
    if len(password) < 8:
        return jsonify({"error": "密码长度不能少于8位"}), 400
    
    # 检查邮箱是否已存在
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.email_verified:
        return jsonify({"error": "该邮箱已被注册"}), 400
    
    # 检查验证码
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "请先获取验证码"}), 400
    
    if user.verification_code != code:
        return jsonify({"error": "验证码错误"}), 400
    
    if user.verification_code_expiry < datetime.datetime.now():
        return jsonify({"error": "验证码已过期"}), 400
    
    # 加密密码
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 更新用户信息
    user.password = hashed_password
    user.email_verified = True
    user.verification_code = None
    user.verification_code_expiry = None
    db.session.commit()
    
    # 生成JWT token
    token = JWTUtil.generate_token(user.id)
    
    return jsonify({"token": token, "email": user.email, "userId": user.user_id}), 201

@bp.route('/login', methods=['POST'])
def login():
    """用户登录API"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "邮箱和密码不能为空"}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": f"邮箱格式无效：{message}"}), 400
    
    # 查找用户
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "邮箱或密码错误"}), 401
    
    # 检查账号是否被锁定
    if user.locked_until and user.locked_until > datetime.datetime.now():
        remaining_time = int((user.locked_until - datetime.datetime.now()).total_seconds() / 60)
        return jsonify({"error": f"账号已被锁定，请{remaining_time}分钟后再试"}), 401
    
    # 验证密码
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # 增加登录失败次数
        user.login_attempts += 1
        
        # 检查是否达到最大登录尝试次数
        if user.login_attempts >= AUTH_CONFIG['max_login_attempts']:
            user.locked_until = datetime.datetime.now() + datetime.timedelta(seconds=AUTH_CONFIG['lock_duration'])
            user.login_attempts = 0
            db.session.commit()
            return jsonify({"error": "登录失败次数过多，账号已被锁定"}), 401
        
        db.session.commit()
        return jsonify({"error": "邮箱或密码错误"}), 401
    
    # 重置登录尝试次数
    user.login_attempts = 0
    user.locked_until = None
    db.session.commit()
    
    # 生成JWT token
    token = JWTUtil.generate_token(user.user_id)
    
    return jsonify({"token": token, "email": user.email, "userId": user.user_id}), 200

@bp.route('/request-reset-password', methods=['POST'])
def request_reset_password():
    """请求重置密码API"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "邮箱不能为空"}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": f"邮箱格式无效：{message}"}), 400
    
    # 查找用户
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "如果该邮箱已注册，重置链接将发送到您的邮箱"}), 200
    
    # 生成重置密码令牌
    reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    
    # 设置重置链接过期时间
    expiry = datetime.datetime.now() + datetime.timedelta(seconds=AUTH_CONFIG['reset_password_expiry'])
    
    # 保存重置令牌到数据库
    user.reset_password_token = reset_token
    user.reset_password_expiry = expiry
    db.session.commit()
    
    # 构建重置链接，域名根据请求头中的Host动态生成
    reset_link = f"{request.url_root.rstrip('/')}/reset-password?token={reset_token}&email={email}"
    
    # 发送重置密码邮件
    success = send_reset_password_email(email, reset_link)
    if success:
        return jsonify({"message": "如果该邮箱已注册，重置链接将发送到您的邮箱"}), 200
    else:
        return jsonify({"error": "发送重置链接失败，请检查邮箱配置或稍后重试"}), 500

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """重置密码API"""
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    new_password = data.get('newPassword')
    
    if not email or not token or not new_password:
        return jsonify({"error": "邮箱、重置令牌和新密码不能为空"}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": f"邮箱格式无效：{message}"}), 400
    
    # 检查密码长度
    if len(new_password) < 8:
        return jsonify({"error": "密码长度不能少于8位"}), 400
    
    # 查找用户
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    # 验证重置令牌
    if user.reset_password_token != token:
        return jsonify({"error": "无效的重置令牌"}), 400
    
    if user.reset_password_expiry < datetime.datetime.now():
        return jsonify({"error": "重置令牌已过期"}), 400
    
    # 加密新密码
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 更新密码并清除重置令牌
    user.password = hashed_password
    user.reset_password_token = None
    user.reset_password_expiry = None
    db.session.commit()
    
    return jsonify({"message": "密码重置成功"}), 200

@bp.route('/refresh', methods=['POST'])
def refresh_token():
    """刷新JWT token API"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "无效的认证头"}), 401
    
    token = auth_header.split(' ')[1]
    user_id = JWTUtil.verify_token(token)
    if not user_id:
        return jsonify({"error": "无效或过期的令牌"}), 401
    
    # 生成新token
    new_token = JWTUtil.generate_token(user_id)
    return jsonify({"token": new_token}), 200

@bp.route('/logout', methods=['POST'])
def logout():
    """用户退出登录API"""
    # JWT是无状态的，退出登录主要在前端清除令牌
    # 这里可以添加额外的退出逻辑，如令牌黑名单等
    return jsonify({"message": "退出登录成功"}), 200