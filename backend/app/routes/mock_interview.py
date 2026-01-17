from flask import Blueprint, request, jsonify
import os
from ..services.deepseek_service import client
from ..services.file_service import get_resume_content
from ..models import db, User, MockInterview, Resume
from ..utils.jwt_utils import auth_required
from ..utils.messages import get_message
from ..utils.prompt_templates import get_system_prompt, get_user_prompt
import uuid

# 创建蓝图
bp = Blueprint('mock_interview', __name__, url_prefix='/api/mock-interview')

def normalize_interviewer_style(style):
    """
    将任何语言的面试官风格规范化为中文（数据库存储格式）
    """
    style_map = {
        # 中文
        '温柔HR': '温柔HR',
        '严厉技术官': '严厉技术官',
        '专业架构师': '专业架构师',
        'CTO': 'CTO',
        # 英文
        'Gentle HR': '温柔HR',
        'Strict Tech Lead': '严厉技术官',
        'Professional Architect': '专业架构师',
        'CTO': 'CTO',
    }
    return style_map.get(style, style)

def get_localized_interviewer_style(style, locale):
    """
    将标准化的中文面试官风格转换为对应语言（用于DeepSeek API）
    """
    if locale == 'en':
        style_map_en = {
            '温柔HR': 'Gentle HR',
            '严厉技术官': 'Strict Tech Lead',
            '专业架构师': 'Professional Architect',
            'CTO': 'CTO',
        }
        return style_map_en.get(style, style)
    else:
        # 中文保持原样
        return style

# 内存中存储面试会话状态 (实际生产环境应使用Redis)
interview_sessions = {}

@bp.route('/start', methods=['POST'])
@auth_required
def start():
    """开始模拟面试API"""
    data = request.get_json()
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    resume_id = data.get('resumeId')  # 允许为空，如果为空则尝试获取用户最新的简历
    style = data.get('style', '温柔HR')
    mode = data.get('mode', 'chat')
    duration = data.get('duration', 15)
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/start - Request received: userId={user_id}, style={style}, mode={mode}, duration={duration}")
    
    if not user_id:
        return jsonify({"error": get_message('missing_params', locale)}), 400
    
    # 规范化面试官风格（支持多语言，存储为标准中文格式）
    style = normalize_interviewer_style(style)
    print(f"[API LOG] Normalized style: {style}")

    # 获取简历ID（如果未提供）
    try:
        if not resume_id:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                # 获取用户最新的简历
                latest_resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.updated_at.desc()).first()
                if latest_resume:
                    resume_id = latest_resume.resume_id
                    print(f"[API LOG] 使用用户最新的简历ID: {resume_id}")
    except Exception as e:
        print(f"获取用户最新简历失败: {e}")
    
    # 获取简历内容
    resume_content = get_resume_content(resume_id, 'optimized')
    if not resume_content:
        # 如果没有内容，使用缺省提示
        resume_content = "（未提供简历内容）"
    
    # 生成interviewId
    interview_id = f"interview_{uuid.uuid4().hex[:8]}"
    
    # 获取本地化的风格名称，用于生成Prompt
    localized_style = get_localized_interviewer_style(style, locale)
    
    # 构建用户Prompt
    user_prompt = get_user_prompt(
        'mock_interview',
        locale,
        'start_interview',
        style=localized_style,
        resume_content=resume_content
    )
    
    # 获取系统Prompt
    system_prompt_template = get_system_prompt('mock_interview', locale, 'interviewer_system')
    # 填充系统Prompt中的变量
    system_prompt = system_prompt_template.format(
        style=localized_style,
        duration=duration,
        resume_content=resume_content
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=8192
        )
        
        import json
        import re
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        
        first_question = {"id": 1, "content": "请介绍一下你自己", "type": "高频必问题"}
        
        if start_idx != -1 and end_idx > start_idx:
            try:
                json_content = api_result[start_idx:end_idx]
                parsed_question = json.loads(json_content)
                if 'content' in parsed_question:
                    first_question = parsed_question
                    # 确保包含必要字段
                    if 'id' not in first_question: first_question['id'] = 1
                    if 'type' not in first_question: first_question['type'] = "高频必问题"
            except Exception as parse_error:
                print(f"JSON解析错误: {parse_error}")
        
        # 保存会话信息
        interview_sessions[interview_id] = {
            "style": style, # 存储标准中文风格
            "mode": mode,
            "duration": duration,
            "resume_id": resume_id,
            "resume_content": resume_content,
            "current_question_id": 1,
            "total_questions": 10,
            "conversation_history": [first_question['content']],
            "question_answers": []
        }
        
        return jsonify({
            "interviewId": interview_id,
            "style": style,
            "mode": mode,
            "duration": duration,
            "currentQuestion": {
                "id": first_question['id'],
                "content": first_question['content'],
                "type": first_question.get('type', '高频必问题')
            },
            "tips": [
                "保持微笑，展现自信",
                "回答问题时保持逻辑清晰",
                "注意控制语速，避免过快或过慢"
            ] if locale == 'zh' else [
                "Keep smiling and show confidence",
                "Maintain logical clarity when answering",
                "Control your speaking pace, avoid too fast or too slow"
            ],
            "message": get_message('interview_started', locale)
        }), 200
        
    except Exception as e:
        print(f"生成第一个问题失败: {e}")
        # 使用默认问题作为备选
        first_question = {"id": 1, "content": "请介绍一下你自己", "type": "高频必问题"}
        
        # 保存会话信息
        interview_sessions[interview_id] = {
            "style": style,
            "mode": mode,
            "duration": duration,
            "resume_id": resume_id,
            "resume_content": resume_content,
            "current_question_id": 1,
            "total_questions": 10,
            "conversation_history": [first_question['content']],
            "question_answers": []
        }
        
        return jsonify({
            "interviewId": interview_id,
            "style": style,
            "mode": mode,
            "duration": duration,
            "currentQuestion": {
                "id": first_question['id'],
                "content": first_question['content'],
                "type": first_question['type']
            },
            "tips": [
                "保持微笑，展现自信",
                "回答问题时保持逻辑清晰",
                "注意控制语速，避免过快或过慢"
            ] if locale == 'zh' else [
                "Keep smiling and show confidence",
                "Maintain logical clarity when answering",
                "Control your speaking pace, avoid too fast or too slow"
            ],
            "message": get_message('interview_started', locale)
        }), 200

@bp.route('/answer', methods=['POST'])
@auth_required
def answer():
    """回答问题API"""
    data = request.get_json()
    interview_id = data.get('interviewId')
    question_id = data.get('questionId')
    answer = data.get('answer')
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/answer - Request received: interviewId={interview_id}, questionId={question_id}, answer={answer[:50]}...")
    
    # 检查会话是否存在
    if interview_id not in interview_sessions:
        return jsonify({"error": get_message('interview_not_found', locale)}), 404
    
    session = interview_sessions[interview_id]
    
    # 保存当前问题和回答
    current_question_text = session["conversation_history"][-1] if session["conversation_history"] else "请介绍一下你自己"
    session["question_answers"].append({
        "question_id": question_id,
        "question": current_question_text,
        "answer": answer
    })
    
    # 获取本地化的风格名称
    localized_style = get_localized_interviewer_style(session['style'], locale)
    
    # 构建用户Prompt
    user_prompt = get_user_prompt(
        'mock_interview',
        locale,
        'feedback_and_question',
        style=localized_style,
        resume_content=session['resume_content'],
        conversation_history=str(session['conversation_history']),
        current_question=current_question_text,
        answer=answer
    )
    
    # 获取系统Prompt
    system_prompt_template = get_system_prompt('mock_interview', locale, 'interviewer_system')
    system_prompt = system_prompt_template.format(
        style=localized_style,
        duration=session['duration'],
        resume_content=session['resume_content']
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=8192
        )
        
        import json
        import re
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_content = api_result[start_idx:end_idx]
            result = json.loads(json_content)
            result["nextQuestion"]["id"] = session["current_question_id"] + 1
        else:
             # Fallback
             result = {
                 "feedback": "...", 
                 "nextQuestion": {"id": session["current_question_id"] + 1, "content": "请继续详细说明一下你的项目经验", "type": "追问"}
             }
        
        # 更新会话信息
        session["current_question_id"] += 1
        session["conversation_history"].append(result["nextQuestion"]["content"])
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"生成反馈和下一个问题失败: {e}")
        return jsonify({"error": get_message('answer_failed', locale, error=str(e))}), 500

@bp.route('/end', methods=['POST'])
@auth_required
def end():
    """结束模拟面试API"""
    data = request.get_json()
    interview_id = data.get('interviewId')
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/end - Request received: interviewId={interview_id}, userId={user_id}")
    
    # 检查会话是否存在
    if interview_id not in interview_sessions:
        return jsonify({"error": get_message('interview_not_found', locale)}), 404
    
    session = interview_sessions[interview_id]
    
    # 获取本地化的风格名称
    localized_style = get_localized_interviewer_style(session['style'], locale)
    
    # 构建用户Prompt
    user_prompt = get_user_prompt(
        'mock_interview',
        locale,
        'generate_report',
        style=localized_style,
        resume_content=session['resume_content'],
        duration=session['duration'],
        question_answers=str(session['question_answers']),
        conversation_history=str(session['conversation_history'])
    )
    
    # 这种情况下系统提示词可以更通用一点
    system_prompt = get_system_prompt('mock_interview', locale, 'interviewer_system').format(
        style=localized_style,
        duration=session['duration'],
        resume_content=session['resume_content']
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=8192
        )
        
        import json
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        
        report = {}
        if start_idx != -1 and end_idx > start_idx:
            json_content = api_result[start_idx:end_idx]
            try:
                report = json.loads(json_content)
            except:
                print("Failed to parse report JSON")

        if not report:
             # Fallback dummy report if parsing fails
             report =  {
                "professionalScore": 80, 
                "logicScore": 80, 
                "confidenceScore": 80, 
                "matchScore": 80,
                "questionAnalysis": [], 
                "optimizationSuggestions": ["多进行实战练习", "加强基础知识"]
             }
        
        # 保存到数据库
        try:      
            # 创建MockInterview记录
            mock_interview = MockInterview(
                user_id=user_id,
                resume_id=session['resume_id'],
                style=session['style'],
                mode=session['mode'],
                duration=session['duration'],
                conversation_history=json.dumps(session['conversation_history']),
                question_answers=json.dumps(session['question_answers']),
                report=json.dumps(report)
            )
            db.session.add(mock_interview)
            db.session.commit()
        except Exception as db_error:
            print(f"保存模拟面试到数据库失败: {db_error}")
        
        # 删除会话信息
        del interview_sessions[interview_id]
        
        return jsonify(report), 200
        
    except Exception as e:
        print(f"生成面试报告失败: {e}")
        
        # 删除会话信息
        del interview_sessions[interview_id]
        
        return jsonify({"error": get_message('end_failed', locale, error=str(e))}), 500

@bp.route('/voice-answer', methods=['POST'])
@auth_required
def voice_answer():
    """语音回答API，处理用户语音输入"""
    locale = request.headers.get('X-Locale', 'zh')
    try:
        # 获取请求数据
        interview_id = request.form.get('interviewId')
        question_id = request.form.get('questionId')
        audio_file = request.files.get('audio')
        
        # 打印请求参数
        print(f"[API LOG] /api/mock-interview/voice-answer - Request received: interviewId={interview_id}, questionId={question_id}")
        
        # 检查会话是否存在
        if interview_id not in interview_sessions:
            return jsonify({"error": get_message('interview_not_found', locale)}), 404
        
        # 保存音频文件到临时目录
        import os
        import tempfile
        from datetime import datetime
        
        # 创建临时目录
        temp_dir = os.path.join(os.getcwd(), 'temp_audio')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # 生成唯一的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = os.path.join(temp_dir, f'{interview_id}_{timestamp}.webm')
        audio_file.save(audio_path)
        
        # 获取语音识别引擎参数，默认使用whisper
        engine = request.form.get('engine', 'whisper')
        
        # 语音识别处理
        transcribed_text = transcribe_audio(audio_path, engine=engine)
        
        # 删除临时文件
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        # 使用现有的answer处理逻辑
        session = interview_sessions[interview_id]
        
        # 保存当前问题和回答
        current_question_text = session["conversation_history"][-1] if session["conversation_history"] else "请介绍一下你自己"
        session["question_answers"].append({
            "question_id": question_id,
            "question": current_question_text,
            "answer": transcribed_text
        })
        
        # 获取本地化的风格名称
        localized_style = get_localized_interviewer_style(session['style'], locale)
        
        # 构建用户Prompt
        user_prompt = get_user_prompt(
            'mock_interview',
            locale,
            'feedback_and_question',
            style=localized_style,
            resume_content=session['resume_content'],
            conversation_history=str(session['conversation_history']),
            current_question=current_question_text,
            answer=transcribed_text
        )
        
        # 获取系统Prompt
        system_prompt_template = get_system_prompt('mock_interview', locale, 'interviewer_system')
        system_prompt = system_prompt_template.format(
            style=localized_style,
            duration=session['duration'],
            resume_content=session['resume_content']
        )
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=8192
            )
            
            import json
            
            # 解析API返回结果
            api_result = response.choices[0].message.content
            
            # 清理可能的额外内容，只保留JSON部分
            start_idx = api_result.find('{')
            end_idx = api_result.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_content = api_result[start_idx:end_idx]
                result = json.loads(json_content)
                result["nextQuestion"]["id"] = session["current_question_id"] + 1
                result["transcribedText"] = transcribed_text
            else:
                 result = {
                     "feedback": "...", 
                     "nextQuestion": {"id": session["current_question_id"] + 1, "content": "请继续", "type": "追问"},
                     "transcribedText": transcribed_text
                 }
            
            # 更新会话信息
            session["current_question_id"] += 1
            session["conversation_history"].append(result["nextQuestion"]["content"])
            
            return jsonify(result), 200
            
        except Exception as e:
            print(f"生成反馈和下一个问题失败: {e}")
            result = {
                     "feedback": "Error generating next question", 
                     "nextQuestion": {"id": session["current_question_id"] + 1, "content": "Please continue", "type": "Follow-up"},
                     "transcribedText": transcribed_text
            }
            return jsonify(result), 200
            
    except Exception as e:
        print(f"语音回答处理失败: {e}")
        return jsonify({"error": get_message('speech_failed', locale, error=str(e))}), 500

@bp.route('/history', methods=['GET'])
@auth_required
def get_history():
    """获取用户的模拟面试历史记录API"""
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    style = request.args.get('style')
    mode = request.args.get('mode')
    duration = request.args.get('duration')
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/history - Request received: userId={user_id}, style={style}, mode={mode}, duration={duration}")
    
    # 规范化面试官风格（支持多语言）
    if style:
        style = normalize_interviewer_style(style)
        print(f"[API LOG] Normalized style: {style}")
    
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    
    try:
        # 获取用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": get_message('user_not_found', locale)}), 404
        
        # 构建查询
        query = MockInterview.query.filter_by(user_id=user_id)
        
        # 添加条件过滤
        if style:
            query = query.filter_by(style=style)
        if mode:
            query = query.filter_by(mode=mode)
        if duration:
            try:
                duration = int(duration)
                query = query.filter_by(duration=duration)
            except ValueError:
                print(f"Invalid duration: {duration}, ignoring")
        
        # 获取最新的一条记录
        mock_interview = query.order_by(MockInterview.created_at.desc()).first()
        
        import json
        
        # 转换为前端需要的格式
        history = []
        if mock_interview:
            history.append({
                "id": mock_interview.id,
                "style": mock_interview.style,
                "mode": mock_interview.mode,
                "duration": mock_interview.duration,
                "resume_id": mock_interview.resume_id,
                "created_at": mock_interview.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "reportData": json.loads(mock_interview.report) if mock_interview.report else {}
            })
        
        # print(f"[API LOG] /api/mock-interview/history - Response: {history}")
        return jsonify(history), 200
    except Exception as e:
        print(f"获取模拟面试历史失败: {e}")
        return jsonify({"error": "Failed to get mock interview history"}), 500

@bp.route('/save-report', methods=['POST'])
@auth_required
def save_report():
    """保存模拟面试报告API"""
    locale = request.headers.get('X-Locale', 'zh')
    try:
        # 获取请求数据
        data = request.get_json()
        # 从request对象中获取用户ID，这是auth_required装饰器设置的
        user_id = request.user_id
        interview_id = data.get('interviewId')
        report_data = data.get('reportData')
        style = data.get('style')
        mode = data.get('mode')
        duration = data.get('duration')
        
        # 规范化面试官风格（支持多语言）
        if style:
            style = normalize_interviewer_style(style)

        resume_id = data.get('resumeId', 'default_resume')
        
        # 打印请求参数
        print(f"[API LOG] /api/mock-interview/save-report - Request received: userId={user_id}, interviewId={interview_id}, style={style}, mode={mode}, duration={duration}")
        
        if not user_id or not report_data:
            return jsonify({"error": get_message('missing_params', locale)}), 400

        import json
        
        # 创建MockInterview记录
        mock_interview = MockInterview(
            user_id=user_id,
            resume_id=resume_id,
            style=style,
            mode=mode,
            duration=duration,
            report=json.dumps(report_data)
        )
        db.session.add(mock_interview)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Report saved successfully", "id": mock_interview.id}), 200
    except Exception as e:
        print(f"保存模拟面试报告失败: {e}")
        return jsonify({"error": "Failed to save mock interview report"}), 500

@bp.route('/realtime-voice', methods=['POST'])
@auth_required
def realtime_voice():
    """实时语音识别API，处理1秒音频分片"""
    locale = request.headers.get('X-Locale', 'zh')
    try:
        interview_id = request.form.get('interviewId')
        question_id = request.form.get('questionId')
        audio_file = request.files.get('audio')
        chunk_index = request.form.get('chunkIndex', 0)
        # 打印调试信息
        print(f"[API LOG] /api/mock-interview/realtime-voice - Received chunk {chunk_index} for interview {interview_id}, question {question_id}")
        
        if not interview_id or not audio_file:
            return jsonify({"error": get_message('missing_params', locale)}), 400
        
        # 保存音频文件到临时目录
        import os
        from datetime import datetime
        import tempfile
        
        temp_dir = os.path.join(os.getcwd(), 'temp_audio')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # 获取原始文件名和扩展名
        original_filename = audio_file.filename
        file_extension = original_filename.split('.')[-1] if original_filename else 'webm'
        
        # 根据实际文件类型保存，不强制使用wav扩展名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        audio_path = os.path.join(temp_dir, f'realtime_{interview_id}_{timestamp}_{chunk_index}.{file_extension}')
        audio_file.save(audio_path)
        
        # 打印保存路径和文件信息
        print(f"[API LOG] /api/mock-interview/realtime-voice - Audio saved to {audio_path}")
        print(f"[API LOG] /api/mock-interview/realtime-voice - File size: {os.path.getsize(audio_path)} bytes")
        print(f"[API LOG] /api/mock-interview/realtime-voice - Original filename: {original_filename}")
        
        # 获取语音识别引擎参数，默认使用whisper
        engine = request.form.get('engine', 'whisper')
        transcribed_text = ""
        
        try:

            # 使用阿里云ASR
            asr_service = get_aliyun_asr_service()
            transcribed_text = asr_service.transcribe_audio(audio_path)
            print(f"[API LOG] /api/mock-interview/realtime-voice - 阿里云ASR识别结果: {transcribed_text}")
                
        except Exception as transcribe_error:
            print(f"[ERROR] 音频转录失败: {transcribe_error}")
            # 返回错误信息
            return jsonify({
                'chunkIndex': chunk_index,
                'error': get_message('speech_failed', locale, error=str(transcribe_error)),
                'status': 'error'
            }), 500
        
        # 删除临时文件
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return jsonify({
            'chunkIndex': chunk_index,
            'transcribedText': transcribed_text,
            'status': 'success'
        }), 200
        
    except Exception as e:
        print(f"实时语音识别失败: {e}")
        return jsonify({
            'chunkIndex': chunk_index if 'chunk_index' in locals() else 0,
            'error': f'处理音频数据失败: {str(e)}',
            'status': 'error'
        }), 500

# 导入阿里云ASR服务
from ..services.aliyun_asr_service import AliyunASRService

# 初始化阿里云ASR服务实例
# 注意：这里使用了懒加载模式，只有在需要时才初始化，避免配置缺失时影响其他功能
_aliyun_asr_service = None

def get_aliyun_asr_service():
    """获取阿里云ASR服务实例（单例模式）"""
    global _aliyun_asr_service
    if _aliyun_asr_service is None:
        try:
            _aliyun_asr_service = AliyunASRService()
        except Exception as e:
            print(f"初始化阿里云ASR服务失败: {e}")
            _aliyun_asr_service = None
    return _aliyun_asr_service

# 语音识别函数
def transcribe_audio(audio_path, engine="whisper"):
    """语音识别函数，支持多种引擎
    
    Args:
        audio_path: 音频文件路径
        engine: 识别引擎，可选值: whisper, aliyun
        
    Returns:
        str: 转录后的文本
    """
    try:
        if engine == "aliyun":
            # 使用阿里云ASR
            asr_service = get_aliyun_asr_service()
            try:
                result = asr_service.transcribe_audio(audio_path)
                print(f"阿里云ASR语音识别结果: {result}")
                return result
            except Exception as aliyun_error:
                print(f"阿里云ASR语音识别失败: {aliyun_error}")
                print("降级使用Faster Whisper")
                # 降级使用Faster Whisper
                engine = "whisper"       
    except Exception as e:
        print(f"语音识别失败: {e}")
    
    # 默认使用Faster Whisper (如果aliyun失败或指定了whisper)
    try:
        from faster_whisper import WhisperModel
        
        # 使用small模型，平衡速度和精度
        model_size = "small"
        
        # 暂不使用GPU，避免某些环境配置问题
        # model = WhisperModel(model_size, device="cuda", compute_type="float16")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        
        segments, info = model.transcribe(audio_path, beam_size=5)
        
        result_text = " ".join([segment.text for segment in segments])
        return result_text.strip()
    except Exception as e:
        print(f"Faster Whisper识别失败: {e}")
        return ""