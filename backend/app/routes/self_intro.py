from flask import Blueprint, request, jsonify
from ..services.deepseek_service import generate_self_intro
from ..services.file_service import get_resume_content
from ..models import db, User, SelfIntro
from ..utils.jwt_utils import auth_required
from ..utils.messages import get_message

# 创建蓝图
bp = Blueprint('self_intro', __name__, url_prefix='/api/self-intro')

def normalize_version_style(version, style):
    """
    将任何语言的版本和风格名称规范化为中文（数据库存储格式）
    """
    # 版本映射
    version_map = {
        # 中文
        '30秒电梯演讲版': '30秒电梯演讲版',
        '1分钟版': '1分钟版',
        '3分钟版': '3分钟版',
        '3分钟标准版': '3分钟版',
        '5分钟深度版': '3分钟版',
        # 英文
        '30s Elevator Pitch': '30秒电梯演讲版',
        '1 Minute Version': '1分钟版',
        '3 Minute Version': '3分钟版',
    }
    
    # 风格映射
    style_map = {
        # 中文
        '正式': '正式',
        '活泼': '活泼',
        '轻松活泼': '活泼',
        '专业': '专业',
        '学术专业': '专业',
        '亲切': '亲切',
        # 英文
        'Formal': '正式',
        'Casual': '活泼',
        'Casual & Lively': '活泼',
        'Academic': '专业',
        'Academic & Professional': '专业',
    }
    
    normalized_version = version_map.get(version, version)
    normalized_style = style_map.get(style, style)
    
    return normalized_version, normalized_style

def get_localized_version_style(version, style, locale):
    """
    将标准化的中文版本/风格转换为对应语言（用于DeepSeek API）
    """
    if locale == 'en':
        # 版本映射到英文
        version_map_en = {
            '30秒电梯演讲版': '30s Elevator Pitch',
            '1分钟版': '1 Minute Version',
            '3分钟版': '3 Minute Version',
        }
        # 风格映射到英文
        style_map_en = {
            '正式': 'Formal',
            '活泼': 'Casual',
            '专业': 'Academic',
            '亲切': 'Friendly',
        }
        return version_map_en.get(version, version), style_map_en.get(style, style)
    else:
        # 中文保持原样
        return version, style


@bp.route('/generate', methods=['POST'])
@auth_required
def generate():
    """根据优化后的简历生成自我介绍API"""
    data = request.get_json()
    version = data.get('version', '30秒电梯演讲版')
    style = data.get('style', '正式')
    user_info = data.get('userInfo', '')
    
    # 规范化版本和风格名称（支持多语言）
    version, style = normalize_version_style(version, style)
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    locale = request.headers.get('X-Locale', 'zh')
    
    # 根据userId获取最新的resumeId
    resume_id = None
    try:
        # 查询用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": get_message('user_not_found', locale)}), 404
        if user:
            # 获取用户最新的简历
            from app.models import Resume
            latest_resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.updated_at.desc()).first()
            if latest_resume:
                resume_id = latest_resume.resume_id
                print(f"[API LOG] 使用用户最新的简历ID: {resume_id}")
    except Exception as e:
        print(f"获取用户最新简历失败: {e}")
    
    # 打印请求参数
    print(f"[API LOG] /api/self-intro/generate - Request received: resumeId={resume_id}, version={version}, style={style}, userInfo={user_info[:50]}..., userId={request.user_id}")
    
    # 根据版本确定预计时长
    estimated_time = "0.5" if version == '30秒电梯演讲版' else "3" if version == '3分钟标准版' else "5"
    
    # 优先使用优化后的简历内容
    resume_content = ""
    if resume_id:
        resume_content = get_resume_content(resume_id, 'optimized')
    
    # 如果没有简历内容，使用userInfo
    if not resume_content:
        resume_content = user_info
    
    # 将version和style转换为locale对应的语言（用于DeepSeek）
    localized_version, localized_style = get_localized_version_style(version, style, locale)
    print(f"[API LOG] Localized params for DeepSeek: version={localized_version}, style={localized_style}, locale={locale}")
    
    # 调用DeepSeek API生成自我介绍
    try:
        intro = generate_self_intro(resume_content, localized_version, localized_style, locale)
        
        # 保存到数据库
        try:
            # 查询用户
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                # 创建自我介绍记录
                self_intro = SelfIntro(
                    user_id=user_id,
                    resume_id=resume_id,
                    self_intro_type=f"{version}_{style}",
                    content=intro
                )
                db.session.add(self_intro)
                db.session.commit()
        except Exception as e:
            print(f"保存自我介绍到数据库失败: {e}")
            db.session.rollback()
        
        return jsonify({
            "intro": intro,
            "version": version,
            "style": style,
            "estimatedTime": estimated_time,
            "message": get_message('intro_generated', locale)
        }), 200
    except Exception as e:
        print(f"生成自我介绍失败: {e}")
        return jsonify({"error": get_message('intro_failed', locale, error=str(e))}), 500

@bp.route('/get', methods=['POST'])
@auth_required
def get_self_intro():
    """获取已生成的自我介绍数据"""
    data = request.get_json()
    if not data:
        return jsonify({"error": get_message('invalid_json', request.headers.get('X-Locale', 'zh'))}), 400
    intro_type = data.get('introType')
    
    # 规范化 introType（支持多语言）
    if intro_type and '_' in intro_type:
        parts = intro_type.split('_', 1)
        version, style = normalize_version_style(parts[0], parts[1])
        intro_type = f"{version}_{style}"
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/self-intro/get - Request received: userId={user_id}, introType={intro_type}")

    if not user_id:
        return jsonify({"error": get_message('missing_params', locale)}), 400
    
    try:
        # 查询用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": get_message('user_not_found', locale)}), 404
        
        # 查询自我介绍数据
        if intro_type:
            # 查询指定类型的最新自我介绍
            self_intro = SelfIntro.query.filter_by(self_intro_type=intro_type, user_id=user_id).order_by(SelfIntro.updated_at.desc()).first()
        else:
            # 查询最新的自我介绍
            self_intro = SelfIntro.query.filter_by(user_id=user_id).order_by(SelfIntro.updated_at.desc()).first()
        
        if not self_intro:
            return jsonify({"error": get_message('get_intro_failed', locale)}), 404
        
        # 提取版本和风格
        version_style = self_intro.self_intro_type.split('_', 1)
        version = version_style[0]
        style = version_style[1] if len(version_style) > 1 else '正式'
        
        # 根据版本确定预计时长
        estimated_time = "0.5" if version == '30秒电梯演讲版' else "3" if version == '3分钟标准版' else "5"
        
        # 构造返回结果
        result = {
            "intro": self_intro.content,
            "version": version,
            "style": style,
            "estimatedTime": estimated_time,
            "resumeId": self_intro.resume_id,
            "userId": user.user_id
        }
        
        return jsonify(result), 200
    except Exception as e:
        print(f"查询自我介绍失败: {e}")
        return jsonify({"error": get_message('get_intro_failed', locale)}), 500
