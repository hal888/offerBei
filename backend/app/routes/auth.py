from flask import Blueprint, request, jsonify
from ..utils.email_utils import EmailUtil
from ..utils.messages import get_message
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

# 发送邮箱验证码 - 使用EmailUtil
def send_verification_email(email, code, locale='zh'):
    try:
        EmailUtil.send_verification_code(email, code, locale)
        return True
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        return False

# 发送密码重置邮件 - 使用EmailUtil
def send_reset_password_email(email, reset_link, locale='zh'):
    try:
        EmailUtil.send_reset_password_link(email, reset_link, locale)
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
    # 优先使用请求体中的locale，如果没有则使用header中的
    locale = data.get('locale') or request.headers.get('X-Locale', 'zh')
    
    if not email:
        return jsonify({"error": get_message('email_required', locale)}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": get_message('email_invalid', locale, error=message)}), 400
    
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
    success = send_verification_email(email, code, locale)
    if success:
        return jsonify({"message": get_message('verification_code_sent', locale)}), 200
    else:
        return jsonify({"error": get_message('send_code_failed', locale)}), 500

@bp.route('/register', methods=['POST'])
def register():
    """用户注册API"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    code = data.get('verificationCode')
    locale = request.headers.get('X-Locale', 'zh')
    
    if not email or not password or not code:
        return jsonify({"error": get_message('email_password_code_required', locale)}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": get_message('email_invalid', locale, error=message)}), 400
    
    # 检查密码长度
    if len(password) < 8:
        return jsonify({"error": get_message('password_min_length', locale)}), 400
    
    # 检查邮箱是否已存在
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.email_verified:
        return jsonify({"error": get_message('email_registered', locale)}), 400
    
    # 检查验证码
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": get_message('get_code_first', locale)}), 400
    
    if user.verification_code != code:
        return jsonify({"error": get_message('code_error', locale)}), 400
    
    if user.verification_code_expiry < datetime.datetime.now():
        return jsonify({"error": get_message('code_expired', locale)}), 400
    
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
    locale = request.headers.get('X-Locale', 'zh')
    
    if not email or not password:
        return jsonify({"error": get_message('email_password_required', locale)}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": get_message('email_invalid', locale, error=message)}), 400
    
    # 查找用户
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": get_message('login_failed', locale)}), 401
    
    # 检查账号是否被锁定
    if user.locked_until and user.locked_until > datetime.datetime.now():
        remaining_time = int((user.locked_until - datetime.datetime.now()).total_seconds() / 60)
        return jsonify({"error": get_message('account_locked', locale, minutes=remaining_time)}), 401
    
    # 验证密码
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # 增加登录失败次数
        user.login_attempts += 1
        
        # 检查是否达到最大登录尝试次数
        if user.login_attempts >= AUTH_CONFIG['max_login_attempts']:
            user.locked_until = datetime.datetime.now() + datetime.timedelta(seconds=AUTH_CONFIG['lock_duration'])
            user.login_attempts = 0
            db.session.commit()
            return jsonify({"error": get_message('login_failure_limit', locale)}), 401
        
        db.session.commit()
        return jsonify({"error": get_message('login_failed', locale)}), 401
    
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
    # 优先使用请求体中的locale，如果没有则使用header中的
    locale = data.get('locale') or request.headers.get('X-Locale', 'zh')
    
    if not email:
        return jsonify({"error": get_message('email_required', locale)}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": get_message('email_invalid', locale, error=message)}), 400
    
    # 查找用户
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": get_message('reset_link_sent', locale)}), 200
    
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
    success = send_reset_password_email(email, reset_link, locale)
    if success:
        return jsonify({"message": get_message('reset_link_sent', locale)}), 200
    else:
        return jsonify({"error": get_message('send_link_failed', locale)}), 500

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """重置密码API"""
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    new_password = data.get('newPassword')
    locale = request.headers.get('X-Locale', 'zh')
    
    if not email or not token or not new_password:
        return jsonify({"error": get_message('email_token_password_required', locale)}), 400
    
    # 验证邮箱格式
    is_valid, message = validate_email_format(email)
    if not is_valid:
        return jsonify({"error": get_message('email_invalid', locale, error=message)}), 400
    
    # 检查密码长度
    if len(new_password) < 8:
        return jsonify({"error": get_message('password_min_length', locale)}), 400
    
    # 查找用户
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": get_message('user_not_found', locale)}), 404
    
    # 验证重置令牌
    if user.reset_password_token != token:
        return jsonify({"error": get_message('invalid_token', locale)}), 400
    
    if user.reset_password_expiry < datetime.datetime.now():
        return jsonify({"error": get_message('token_expired', locale)}), 400
    
    # 加密新密码
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 更新密码并清除重置令牌
    user.password = hashed_password
    user.reset_password_token = None
    user.reset_password_expiry = None
    db.session.commit()
    
    return jsonify({"message": get_message('password_reset_success', locale)}), 200

@bp.route('/refresh', methods=['POST'])
def refresh_token():
    """刷新JWT token API"""
    auth_header = request.headers.get('Authorization')
    locale = request.headers.get('X-Locale', 'zh')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": get_message('invalid_auth_header', locale)}), 401
    
    token = auth_header.split(' ')[1]
    user_id = JWTUtil.verify_token(token)
    if not user_id:
        return jsonify({"error": get_message('invalid_token_error', locale)}), 401
    
    # 生成新token
    new_token = JWTUtil.generate_token(user_id)
    return jsonify({"token": new_token}), 200

@bp.route('/logout', methods=['POST'])
def logout():
    """用户退出登录API"""
    # JWT是无状态的，退出登录主要在前端清除令牌
    # 这里可以添加额外的退出逻辑，如令牌黑名单等
    locale = request.headers.get('X-Locale', 'zh')
    return jsonify({"message": get_message('logout_success', locale)}), 200