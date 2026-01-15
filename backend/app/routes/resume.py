from flask import Blueprint, request, jsonify
import os
from ..services.file_service import read_file_content, save_resume
from ..services.deepseek_service import analyze_resume
from ..utils.json_parser import parse_resume_result
from ..models import db, User, Resume
from ..utils.jwt_utils import auth_required
from ..utils.messages import get_message
import uuid

# 创建蓝图
bp = Blueprint('resume', __name__, url_prefix='/api/resume')

@bp.route('/analyze', methods=['POST'])
@auth_required
def analyze():
    """简历分析API"""
    # 从认证中间件获取user_id
    user_id = request.user_id
    locale = request.headers.get('X-Locale', 'zh')
    # 打印请求参数user_id
    print(f"[API LOG] /api/resume/analyze - Request received: user_id={user_id}, files={[f.filename for f in request.files.values()]}, form_data={dict(request.form)}")
    
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({"error": get_message('file_required', locale)}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": get_message('file_empty', locale)}), 400
    
    
    
    # 获取文件信息
    filename = file.filename
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # 保存文件到临时目录
    temp_dir = '/tmp/resume_uploads'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_path = os.path.join(temp_dir, filename)
    file.save(file_path)
    
    # 读取文件内容
    file_content = read_file_content(file_path, file_ext)
    content_length = len(file_content)
    
    # 文件内容写入文件
    # with open('resume.txt', 'w', encoding='utf-8') as f:
    #     f.write(file_content)
    
    # if not file_content:
    #     # 清理临时文件
    #     if os.path.exists(file_path):
    #         os.remove(file_path)
    #     return jsonify({"error": "无法读取文件内容"}), 400
    
    # 调用DeepSeek API进行简历分析
    api_result = analyze_resume(file_content)
    
    # 解析API返回结果
    parsed_result = parse_resume_result(api_result)
    # print(parsed_result)
    
    # 生成唯一的resume_id，用于原始和优化后的简历
    resume_id = uuid.uuid4().hex[:8]
    
    # 保存原始简历内容到文件系统，使用统一的resume_id
    save_resume(file_content, 'original', resume_id)
    
    # 保存优化后的简历内容到文件系统，使用相同的resume_id
    if parsed_result['optimizedResume']:
        save_resume(parsed_result['optimizedResume'], 'optimized', resume_id)
    
    # 保存到数据库，resume_id为统一生成的id（即优化后的简历id）
    try:
       
        # 创建简历记录，resume_id为统一生成的id
        resume = Resume(
            resume_id=resume_id,
            user_id=user_id,
            original_content=file_content,
            optimized_content=parsed_result['optimizedResume'],
            score=parsed_result['score'],
            diagnosis=parsed_result['diagnosis'],
            keywords=parsed_result['keywords'],
            star_rewrite=parsed_result['starRewrite']
        )
        db.session.add(resume)
        db.session.commit()
    except Exception as e:
        print(f"保存简历到数据库失败: {e}")
        db.session.rollback()
    
    # 清理临时文件
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # 生成最终的分析结果
    analysis_result = {
        "score": parsed_result["score"],
        "diagnosis": parsed_result["diagnosis"],
        "keywords": parsed_result["keywords"],
        "starRewrite": parsed_result["starRewrite"],
        "optimizedResume": parsed_result["optimizedResume"],
        "fileInfo": {
            "filename": filename,
            "fileType": file_ext,
            "contentLength": content_length
        },
        "apiResponse": api_result,  # 保留原始API响应，方便调试
        "resumeId": resume_id,
        "userId": user_id  # 返回user_id，前端保存到localStorage
    }
    
    return jsonify(analysis_result), 200

@bp.route('/get', methods=['POST'])
@auth_required
def get_resume():
    """获取已生成的简历数据"""
    data = request.get_json()
    resume_id = data.get('resumeId')
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/resume/get - Request received: userId={user_id}, resumeId={resume_id}")
    
    if not user_id:
        return jsonify({"error": get_message('user_not_found', locale)}), 400
    
    try:
        # 查询用户
        # user = User.query.filter_by(user_id=user_id).first()
        # if not user:
        #     return jsonify({"error": "User not found"}), 404
        
        # 查询简历数据
        if resume_id:
            # 查询指定resume_id的简历
            resume = Resume.query.filter_by(resume_id=resume_id, user_id=user_id).first()
        else:
            # 查询最新的简历
            resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.updated_at.desc()).first()
        
        if not resume:
            # Resume not found usually means user hasn't uploaded one yet
            # In English: "Resume not found" or "Please upload resume first" depending on context,
            # but here "Resume not found" is accurate.
            # Using 'analysis_failed' key might not be appropriate, let's use a generic error or add new one.
            # Adding 'resume_not_found' to messages would be better, but for now I'll use 'analysis_failed' with a custom error message if needed, or better yet, reuse 'user_not_found' logic or just return 404 with standard message?
            # Actually, the implementation plan said to use get_message.
            # I will assume 'resume_not_found' or similar, but I didn't add it to messages.py.
            # The existing code returned "Resume not found".
            # I will use 'analyzing_failed' with "Resume not found" as error, or simply return empty result?
            # Front end likely expects 404.
            # Let's check messages.py again.
            # I have 'resume_required': 'Please upload resume first'. This is close.
            return jsonify({"error": get_message('resume_required', locale)}), 404
        
        # 构造返回结果
        result = {
            "score": resume.score,
            "diagnosis": resume.diagnosis,
            "keywords": resume.keywords,
            "starRewrite": resume.star_rewrite,
            "optimizedResume": resume.optimized_content,
            "resumeId": resume.resume_id,
            "userId": user_id
        }
        
        return jsonify(result), 200
    except Exception as e:
        print(f"查询简历失败: {e}")
        return jsonify({"error": get_message('analysis_failed', locale, error="Failed to get resume")}), 500
