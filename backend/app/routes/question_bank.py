from flask import Blueprint, request, jsonify
import os
from ..services.deepseek_service import client
from ..services.file_service import get_resume_content
from ..models import db, User, QuestionBank
from ..utils.jwt_utils import auth_required
import uuid

# 创建蓝图
bp = Blueprint('question_bank', __name__, url_prefix='/api/question-bank')

@bp.route('/generate', methods=['POST'])
@auth_required
def generate():
    """"基于简历内容生成智能题库API"""""
    data = request.get_json()
    count = data.get('count', 10)  # 默认生成10个问题
    topic = data.get('topic', '')
    user_id = data.get('userId') or str(uuid.uuid4())
    
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
    
    # 打印请求参数
    print(f"[API LOG] /api/question-bank/generate - Request received: resumeId={resume_id}, count={count}, topic={topic}, userId={user_id}")
    
    # 获取简历内容
    resume_content = get_resume_content(resume_id, 'optimized')
    
    # 如果没有优化简历，尝试获取原始简历
    if not resume_content:
        resume_content = get_resume_content(resume_id, 'original')
    
    # 如果没有简历内容，使用示例简历
    if not resume_content:
        resume_content = "# 示例简历\n\n## 个人信息\n张三 | 前端开发工程师\n\n## 工作经历\n2020-至今 某互联网公司 前端开发工程师\n- 负责公司核心产品的前端开发\n- 熟练使用Vue、React等前端框架\n- 参与过多个大型项目的开发\n\n## 教育背景\n2016-2020 某大学 计算机科学与技术 本科\n\n## 技能\n- 前端框架：Vue、React、Angular\n- 编程语言：JavaScript、TypeScript、HTML、CSS\n- 其他技能：Git、Webpack、Node.js"
    
    
    # 构建基于话题的prompt
    if topic:
        prompt = f"""
        请基于以下简历内容和指定话题，生成{count}个与候选人背景和话题紧密相关的面试问题，涵盖高频必问题、简历深挖题、专业技能题和行为/情景题等类型。
        
        ## 指定话题：
        {topic}
        
        ## 简历内容：
        {resume_content}
        
        ## 输出要求：
        1. 仅输出JSON字符串，不要包含任何额外的文字、解释或说明
        2. JSON格式必须严格有效，使用双引号，转义所有特殊字符
        3. 确保所有字段类型正确
        4. 每个问题必须包含：
           - `id`: 唯一标识符（从1开始递增）
           - `content`: 问题内容
           - `type`: 问题类型（高频必问题/简历深挖题/专业技能题/行为/情景题）
           - `answer`: 参考答案或回答思路
           - `analysis`: 问题分析或考察目的
        5. 问题必须同时与候选人的简历内容和指定话题紧密相关，突出话题与候选人背景的结合点
        6. 问题类型要多样化，覆盖不同的考察维度
        7. 重点围绕指定话题设计专业技能题和行为/情景题
        
        ## 示例输出格式：
        ```json
        {{"questions":[{{"id":1,"content":"请介绍一下你在电商项目中负责的主要工作","type":"简历深挖题","answer":"建议使用STAR法则回答","analysis":"考察候选人的项目经验和职责理解"}}],"total":1}}
        ```
        """
    else:
        prompt = f"""
        请基于以下简历内容，生成{count}个与候选人背景相关的面试问题，涵盖高频必问题、简历深挖题、专业技能题和行为/情景题等类型。
        
        ## 简历内容：
        {resume_content}
        
        ## 输出要求：
        1. 仅输出JSON字符串，不要包含任何额外的文字、解释或说明
        2. JSON格式必须严格有效，使用双引号，转义所有特殊字符
        3. 确保所有字段类型正确
        4. 每个问题必须包含：
           - `id`: 唯一标识符（从1开始递增）
           - `content`: 问题内容
           - `type`: 问题类型（高频必问题/简历深挖题/专业技能题/行为/情景题）
           - `answer`: 参考答案或回答思路
           - `analysis`: 问题分析或考察目的
        5. 问题必须与候选人的简历内容紧密相关，不要生成与简历无关的问题
        6. 问题类型要多样化，覆盖不同的考察维度
        
        ## 示例输出格式：
        ```json
        {{"questions":[{{"id":1,"content":"请介绍一下你在电商项目中负责的主要工作","type":"简历深挖题","answer":"建议使用STAR法则回答","analysis":"考察候选人的项目经验和职责理解"}}],"total":1}}
        ```
        """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位专业的面试问题生成专家，擅长根据候选人的简历内容生成相关的面试问题"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=8192
        )
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        # 保存原始响应到文件，便于调试
        # with open('question_bank_response.txt', 'w', encoding='utf-8') as f:
        #     f.write(api_result)
        
        # 解析JSON响应
        import json
        import re
        
        # 清理Markdown代码块和额外内容
        cleaned_response = api_result
        
        # 移除Markdown代码块标记
        if cleaned_response.startswith('```json') or cleaned_response.startswith('```'):
            # 找到第一个换行后的内容
            cleaned_response = cleaned_response.split('\n', 1)[1]
        if cleaned_response.endswith('```'):
            # 找到最后一个换行前的内容
            cleaned_response = cleaned_response.rsplit('\n', 1)[0]
        
        # 清理可能的额外内容，只保留JSON部分
        start_idx = cleaned_response.find('{')
        end_idx = cleaned_response.rfind('}') + 1
        if start_idx == -1 or end_idx <= start_idx:
            print(f"无法找到有效的JSON结构: {cleaned_response}")
            return jsonify({"error": "API返回格式错误，无法解析JSON"}), 500
        
        json_content = cleaned_response[start_idx:end_idx]
        
        # 清理无效控制字符
        json_content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', json_content)
        
        # 尝试解析JSON
        try:
            result = json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print(f"原始JSON内容: {json_content}")
            return jsonify({"error": "API返回格式错误，无法解析JSON"}), 500
        
        # 保存到数据库
        try:
            # 查询或创建用户
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                user = User(user_id=user_id)
                db.session.add(user)
                db.session.commit()  # 立即提交，获取user_id
            
            # 创建题库记录
            question_bank = QuestionBank(
                user_id=user_id,
                resume_id=resume_id,
                count=count,
                questions=result.get("questions", [])
            )
            db.session.add(question_bank)
            db.session.commit()
        except Exception as e:
            print(f"保存题库到数据库失败: {e}")
            db.session.rollback()
        
        # 获取生成的问题列表
        questions_list = result.get("questions", [])
        
        # 添加调试日志
        print(f"[DEBUG] 成功生成题库: 问题数量={len(questions_list)}")
        print(f"[DEBUG] 返回响应结构: questions数量={len(questions_list)}, total={len(questions_list)}, topic={topic}, userId={user_id}")
        
        response_data = {
            "questions": questions_list,
            "total": len(questions_list),  # 从实际问题数量计算，而不是依赖LLM返回的total字段
            "topic": topic,
            "userId": user_id  # 返回user_id，前端保存到localStorage
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"生成题库失败: {e}")
        return jsonify({"error": "生成题库失败，请重试"}), 500

@bp.route('/get', methods=['POST'])
@auth_required
def get_question_bank():
    """获取已生成的智能题库数据"""
    data = request.get_json()
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    resume_id = data.get('resumeId')  # 允许为空
    count = data.get('count')  # 新增：获取题目数量筛选条件
    
    # 打印请求参数
    print(f"[API LOG] /api/question-bank/get - Request received: userId={user_id}, resumeId={resume_id}, count={count}")
    
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400
    
    try:
        # 查询用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # 查询题库数据
        filters = {"user_id": user_id}
        if resume_id:
            filters["resume_id"] = resume_id
        if count and isinstance(count, int) and count > 0:
            filters["count"] = count
        
        # 查询匹配的题库
        question_bank = QuestionBank.query.filter_by(**filters).order_by(QuestionBank.updated_at.desc()).first()
        
        if not question_bank:
            return jsonify({"questions": [], "total": 0}), 200
        
        # 构造返回结果
        result = {
            "questions": question_bank.questions,
            "total": len(question_bank.questions),
            "count": question_bank.count,
            "resumeId": question_bank.resume_id,
            "userId": user.user_id
        }
        
        return jsonify(result), 200
    except Exception as e:
        print(f"查询题库失败: {e}")
        return jsonify({"error": "Failed to get question bank"}), 500
