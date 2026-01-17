from flask import Blueprint, request, jsonify
import os
from ..services.deepseek_service import client
from ..services.file_service import get_resume_content
from ..models import db, User, QuestionBank
from ..utils.jwt_utils import auth_required
from ..utils.messages import get_message
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils.prompt_templates import get_system_prompt, get_user_prompt

# 创建蓝图
bp = Blueprint('question_bank', __name__, url_prefix='/api/question-bank')

def _generate_single_batch(client, resume_content, topic, batch_count, locale='zh'):
    """
    生成单批题目的辅助函数
    
    Args:
        client: DeepSeek客户端
        resume_content: 简历内容
        topic: 自定义话题
        batch_count: 本批生成数量
        locale: 语言设置 ('zh' 或 'en')
        
    Returns:
        list: 问题列表，失败返回空列表
    """
    import json
    import re
    
    # 使用prompt模板系统生成locale-aware的prompt
    user_prompt = get_user_prompt(
        'question_bank',
        locale,
        'user_template',
        count=batch_count,
        resume_content=resume_content,
        custom_topic=topic if topic else ""
    )
    
    system_prompt = get_system_prompt('question_bank', locale)
    
    # 计算max_tokens
    max_tokens = min(int((500 + 600 * batch_count) * 1.2), 8192)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        
        api_result = response.choices[0].message.content
        
        # 清理JSON
        cleaned = api_result
        if cleaned.startswith('```json') or cleaned.startswith('```'):
            cleaned = cleaned.split('\n', 1)[1]
        if cleaned.endswith('```'):
            cleaned = cleaned.rsplit('\n', 1)[0]
        
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}') + 1
        if start_idx == -1 or end_idx <= start_idx:
            return []
        
        json_content = cleaned[start_idx:end_idx]
        json_content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', json_content)
        
        result = json.loads(json_content)
        return result.get("questions", [])
        
    except Exception as e:
        print(f"批次生成失败: {e}")
        return []

@bp.route('/generate', methods=['POST'])
@auth_required
def generate():
    """"基于简历内容生成智能题库API"""""
    data = request.get_json()
    count = data.get('count', 10)  # 默认生成10个问题
    topic = data.get('topic', '')
    user_id = data.get('userId') or str(uuid.uuid4())
    locale = request.headers.get('X-Locale', 'zh')
    
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
    
    # 判断是否需要分批生成
    all_questions = []
    
    if count > 15:
        # 大量题目，并发分批生成（每批10题）
        batch_size = 10
        num_batches = (count + batch_size - 1) // batch_size
        print(f"[DEBUG] 题目数量{count}，分{num_batches}批并发生成，每批{batch_size}题")
        
        # 准备所有批次的参数
        batch_tasks = []
        for batch_idx in range(num_batches):
            remaining = count - len(batch_tasks) * batch_size
            current_batch_size = min(batch_size, remaining)
            batch_tasks.append((batch_idx, current_batch_size, num_batches))
        
        # 使用线程池并发执行所有批次
        with ThreadPoolExecutor(max_workers=min(num_batches, 5)) as executor:
            # 提交所有批次任务
            future_to_batch = {
                executor.submit(_generate_single_batch, client, resume_content, topic, task[1], locale): task[0]
                for task in batch_tasks
            }
            
            # 收集结果
            for future in as_completed(future_to_batch):
                batch_idx = future_to_batch[future]
                try:
                    batch_questions = future.result()
                    all_questions.extend(batch_questions)
                    print(f"[DEBUG] 批次{batch_idx + 1}完成: {len(batch_questions)}题")
                except Exception as e:
                    print(f"[DEBUG] 批次{batch_idx + 1}失败: {e}")
        
        if not all_questions:
            return jsonify({"error": get_message('generate_failed', locale, error="All batches failed")}), 500
        
        result = {"questions": all_questions}
        print(f"[DEBUG] 并发生成完成，共{len(all_questions)}题")
        
    else:
        # 少量题目，单次生成
        print(f"[DEBUG] 单次生成{count}题")
        questions = _generate_single_batch(client, resume_content, topic, count, locale)
        
        if not questions:
            return jsonify({"error": get_message('generate_failed', locale, error="Generation failed")}), 500
        
        result = {"questions": questions}
    
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
    

@bp.route('/get', methods=['POST'])
@auth_required
def get_question_bank():
    """获取已生成的智能题库数据"""
    data = request.get_json()
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    resume_id = data.get('resumeId')  # 允许为空
    count = data.get('count')  # 新增：获取题目数量筛选条件
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/question-bank/get - Request received: userId={user_id}, resumeId={resume_id}, count={count}")
    
    if not user_id:
        return jsonify({"error": get_message('missing_params', locale)}), 400
    
    try:
        # 查询用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": get_message('user_not_found', locale)}), 404
        
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
        return jsonify({"error": get_message('get_question_bank_failed', locale)}), 500
