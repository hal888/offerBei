from flask import Blueprint, request, jsonify
import random
import uuid
import json
from ..services.deepseek_service import client
from ..services.file_service import get_resume_content
from ..models import db, User, MockInterview
from ..utils.jwt_utils import auth_required

# 创建蓝图
bp = Blueprint('mock_interview', __name__, url_prefix='/api/mock-interview')

# 保存面试会话的字典（生产环境中应使用数据库）
interview_sessions = {}

@bp.route('/start', methods=['POST'])
@auth_required
def start():
    """开始模拟面试API"""
    data = request.get_json()
    style = data.get('style', '温柔HR')
    mode = data.get('mode', '文字模式')
    duration = data.get('duration', 15)
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/start - Request received: style={style}, mode={mode}, duration={duration}, userId={user_id}")
    
    # 根据userId获取最新的resumeId
    resume_id = '1'  # 默认值
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            # 获取用户最新的简历
            from app.models import Resume
            latest_resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.updated_at.desc()).first()
            if latest_resume:
                resume_id = latest_resume.resume_id
                print(f"[API LOG] 使用用户最新的简历ID: {resume_id}")
    except Exception as e:
        print(f"获取用户最新简历失败: {e}")
    
    # 获取简历内容
    resume_content = get_resume_content(resume_id, 'optimized')
    
    # 生成interviewId
    interview_id = f"interview_{uuid.uuid4().hex[:8]}"
    
    # 构建prompt生成第一个问题（使用字符串连接避免格式说明符问题）
    prompt = "你是一位" + style + "风格的面试官，正在为候选人进行面试。请基于以下简历内容，生成第一个面试问题，要求：\n\n1. 问题类型：高频必问题（如自我介绍、求职动机等）\n2. 问题要与候选人的简历背景相关\n3. 语言风格符合" + style + "特点\n4. 仅输出JSON格式，包含id、content、type字段\n5. 不要包含任何额外的文字或解释\n\n简历内容：\n" + resume_content
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位" + style + "风格的专业面试官"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=512
        )
        
        import json
        import re
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        if start_idx == -1 or end_idx <= start_idx:
            # 如果解析失败，使用默认问题
            first_question = {"id": 1, "content": "请介绍一下你自己", "type": "高频必问题"}
        else:
            json_content = api_result[start_idx:end_idx]
            first_question = json.loads(json_content)
        
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
            "tips": ["保持微笑，展现自信", "回答问题时保持逻辑清晰", "注意控制语速，避免过快或过慢"]
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
            "tips": ["保持微笑，展现自信", "回答问题时保持逻辑清晰", "注意控制语速，避免过快或过慢"]
        }), 200

@bp.route('/answer', methods=['POST'])
@auth_required
def answer():
    """回答问题API"""
    data = request.get_json()
    interview_id = data.get('interviewId')
    question_id = data.get('questionId')
    answer = data.get('answer')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/answer - Request received: interviewId={interview_id}, questionId={question_id}, answer={answer[:50]}...")
    
    # 检查会话是否存在
    if interview_id not in interview_sessions:
        return jsonify({"error": "面试会话不存在"}), 404
    
    session = interview_sessions[interview_id]
    
    # 保存当前问题和回答
    session["question_answers"].append({
        "question_id": question_id,
        "question": session["conversation_history"][-1] if session["conversation_history"] else "请介绍一下你自己",
        "answer": answer
    })
    
    # 构建prompt生成反馈和下一个问题（使用字符串连接避免格式说明符问题）
    current_question = session["conversation_history"][-1] if session["conversation_history"] else "请介绍一下你自己"
    prompt = "你是一位" + session['style'] + "风格的面试官，正在为候选人进行面试。请基于以下信息：\n\n1. 简历内容：" + session['resume_content'] + "\n2. 对话历史：" + str(session['conversation_history']) + "\n3. 当前问题：" + current_question + "\n4. 候选人回答：" + answer + "\n\n请完成以下任务：\n\n1. 生成对当前回答的反馈，要求：\n   - 评价回答的质量、逻辑、深度\n   - 指出优点和不足\n   - 语言风格符合" + session['style'] + "\n\n2. 生成下一个面试问题，要求：\n   - 问题类型多样（简历深挖题、专业技能题、行为/情景题等）\n   - 与候选人的简历和对话历史相关\n   - 难度适中，符合面试流程\n\n输出格式要求：\n{\"feedback\": \"对当前回答的反馈\", \"nextQuestion\": {\"id\": 数字id, \"content\": \"下一个问题内容\", \"type\": \"问题类型\"}}\n\n只输出JSON格式，不要包含任何额外的文字或解释。"
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位" + session['style'] + "风格的专业面试官"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        import json
        import re
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        if not (start_idx == -1 or end_idx <= start_idx):
            json_content = api_result[start_idx:end_idx]
            result = json.loads(json_content)
            result["nextQuestion"]["id"] = session["current_question_id"] + 1
        
        # 更新会话信息
        session["current_question_id"] += 1
        session["conversation_history"].append(result["nextQuestion"]["content"])
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"生成反馈和下一个问题失败: {e}")
        
        return jsonify(result), 200

@bp.route('/end', methods=['POST'])
@auth_required
def end():
    """结束模拟面试API"""
    data = request.get_json()
    interview_id = data.get('interviewId')
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/end - Request received: interviewId={interview_id}, userId={user_id}")
    
    # 检查会话是否存在
    if interview_id not in interview_sessions:
        return jsonify({"error": "面试会话不存在"}), 404
    
    session = interview_sessions[interview_id]
    
    # 构建prompt生成面试报告（使用字符串连接避免格式说明符问题）
    prompt = "你是一位专业的面试评估专家，正在为候选人生成面试报告。请基于以下信息：\n\n1. 简历内容：" + session['resume_content'] + "\n2. 面试风格：" + session['style'] + "\n3. 面试时长：" + str(session['duration']) + "分钟\n4. 问答记录：" + str(session['question_answers']) + "\n5. 对话历史：" + str(session['conversation_history']) + "\n\n请生成一份详细的面试报告，要求：\n\n1. 包含以下评分项（0-100分）：\n   - professionalScore：专业能力评分\n   - logicScore：逻辑表达评分\n   - confidenceScore：自信程度评分\n   - matchScore：岗位匹配度评分\n\n2. 逐题诊断，每个问题包含：\n   - question：问题内容\n   - answer：候选人回答\n   - feedback：对该回答的评价\n   - suggestion：改进建议\n\n3. 优化建议，包含至少4条针对性建议\n\n输出格式要求：\n{\"professionalScore\": 数字, \"logicScore\": 数字, \"confidenceScore\": 数字, \"matchScore\": 数字, \"questionAnalysis\": [{\"question\": \"问题内容\", \"answer\": \"候选人回答\", \"feedback\": \"评价\", \"suggestion\": \"改进建议\"}], \"optimizationSuggestions\": [\"建议1\", \"建议2\"]}\n\n只输出JSON格式，不要包含任何额外的文字或解释。"
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位专业的面试评估专家"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = api_result.find('{')
        end_idx = api_result.rfind('}') + 1
        if not (start_idx == -1 or end_idx <= start_idx):
            json_content = api_result[start_idx:end_idx]
            report = json.loads(json_content)
        
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
        
        return jsonify(report), 200

@bp.route('/voice-answer', methods=['POST'])
@auth_required
def voice_answer():
    """语音回答API，处理用户语音输入"""
    try:
        # 获取请求数据
        interview_id = request.form.get('interviewId')
        question_id = request.form.get('questionId')
        audio_file = request.files.get('audio')
        
        # 打印请求参数
        print(f"[API LOG] /api/mock-interview/voice-answer - Request received: interviewId={interview_id}, questionId={question_id}")
        
        # 检查会话是否存在
        if interview_id not in interview_sessions:
            return jsonify({"error": "面试会话不存在"}), 404
        
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
        
        # 语音识别处理
        transcribed_text = transcribe_audio(audio_path)
        
        # 删除临时文件
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        # 使用现有的answer处理逻辑
        session = interview_sessions[interview_id]
        
        # 保存当前问题和回答
        current_question = session["conversation_history"][-1] if session["conversation_history"] else "请介绍一下你自己"
        session["question_answers"].append({
            "question_id": question_id,
            "question": current_question,
            "answer": transcribed_text
        })
        
        # 构建prompt生成反馈和下一个问题（使用字符串连接避免格式说明符问题）
        prompt = "你是一位" + session['style'] + "风格的面试官，正在为候选人进行面试。请基于以下信息：\n\n1. 简历内容：" + session['resume_content'] + "\n2. 对话历史：" + str(session['conversation_history']) + "\n3. 当前问题：" + current_question + "\n4. 候选人回答：" + transcribed_text + "\n\n请完成以下任务：\n\n1. 生成对当前回答的反馈，要求：\n   - 评价回答的质量、逻辑、深度\n   - 指出优点和不足\n   - 语言风格符合" + session['style'] + "\n\n2. 生成下一个面试问题，要求：\n   - 问题类型多样（简历深挖题、专业技能题、行为/情景题等）\n   - 与候选人的简历和对话历史相关\n   - 难度适中，符合面试流程\n\n输出格式要求：\n{\"feedback\": \"对当前回答的反馈\", \"nextQuestion\": {\"id\": 数字id, \"content\": \"下一个问题内容\", \"type\": \"问题类型\"}}\n\n只输出JSON格式，不要包含任何额外的文字或解释。"
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位" + session['style'] + "风格的专业面试官"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            # 解析API返回结果
            api_result = response.choices[0].message.content
            
            # 清理可能的额外内容，只保留JSON部分
            start_idx = api_result.find('{')
            end_idx = api_result.rfind('}') + 1
            if not (start_idx == -1 or end_idx <= start_idx):
                json_content = api_result[start_idx:end_idx]
                result = json.loads(json_content)
                result["nextQuestion"]["id"] = session["current_question_id"] + 1
                result["transcribedText"] = transcribed_text
            
            # 更新会话信息
            session["current_question_id"] += 1
            session["conversation_history"].append(result["nextQuestion"]["content"])
            
            return jsonify(result), 200
            
        except Exception as e:
            print(f"生成反馈和下一个问题失败: {e}")
            
            return jsonify(result), 200
            
    except Exception as e:
        print(f"语音回答处理失败: {e}")
        return jsonify({"error": "语音回答处理失败"}), 500

@bp.route('/history', methods=['GET'])
@auth_required
def get_history():
    """获取用户的模拟面试历史记录API"""
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    style = request.args.get('style')
    mode = request.args.get('mode')
    duration = request.args.get('duration')
    
    # 打印请求参数
    print(f"[API LOG] /api/mock-interview/history - Request received: userId={user_id}, style={style}, mode={mode}, duration={duration}")
    
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    
    try:
        # 获取用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
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
        resume_id = data.get('resumeId', 'default_resume')
        
        # 打印请求参数
        print(f"[API LOG] /api/mock-interview/save-report - Request received: userId={user_id}, interviewId={interview_id}, style={style}, mode={mode}, duration={duration}")
        
        if not user_id or not report_data:
            return jsonify({"error": "Missing required parameters"}), 400

        
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

# 语音识别函数
def transcribe_audio(audio_path):
    """将音频文件转换为文本"""
    try:
        # 这里使用OpenAI Whisper API进行语音识别
        # 实际部署时需要替换为真实的API调用或本地模型
        import openai
        import os
        
        # 检查是否设置了API密钥
        if not os.environ.get('OPENAI_API_KEY'):
            # 如果没有API密钥，返回模拟结果
            print("未设置OPENAI_API_KEY，使用模拟语音识别结果")
            return "这是一个模拟的语音识别结果。在实际环境中，这里会调用真实的语音识别API，如OpenAI Whisper，将音频文件转换为准确的文本内容。"
        
        # 使用OpenAI Whisper API
        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file, language="zh")
        
        return transcript["text"]
    except Exception as e:
        print(f"语音识别失败: {e}")
        # 返回模拟结果
        return "这是一个模拟的语音识别结果。在实际环境中，这里会调用真实的语音识别API，如OpenAI Whisper，将音频文件转换为准确的文本内容。"