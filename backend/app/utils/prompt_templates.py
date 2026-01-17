# -*- coding: utf-8 -*-
"""
多语言Prompt模板管理器
用于DeepSeek API调用的中英文Prompt模板
"""

PROMPTS = {
    'zh': {
        # ===== 简历分析 =====
        'resume_analysis': {
            'system': '你是一位专业的简历分析专家，擅长评估技术岗位的简历',
            'user_template': '''请对以下简历内容进行全面分析和优化，并严格按照以下要求输出JSON格式结果：

## 输出要求：
1. **仅输出JSON字符串**，不要包含任何额外的文字、解释或说明
2. JSON格式必须严格有效，使用双引号，转义所有特殊字符（如换行符\\n）
3. 确保所有字段类型正确
4. **重要**：在JSON字符串值内部不要使用双引号，如需引用请使用单引号

## 必须包含的字段：
- `score`: 整数，0-100分的综合评分
- `diagnosis`: 数组，每条诊断包含`type`(警告/错误/建议)、`title`、`description`
- `keywords`: 数组，至少10个与技术岗位相关的关键词
- `starRewrite`: 数组，每条STAR包含`situation`、`task`、`action`、`result`
- `optimizedResume`: 字符串，完整的优化后简历内容，**必须使用美观的Markdown格式**

## 优化后简历（optimizedResume）的格式要求：
1. 使用清晰的Markdown层级结构
2. 标题使用`#`、`##`、`###`等标记
3. 工作经历按时间倒序排列
4. 重点突出量化结果和关键成就

简历内容：
{resume_content}'''
        },
        
        # ===== 自我介绍 =====
        'self_intro': {
            'system': '你是一位专业的自我介绍生成专家，擅长生成自然、流畅、有吸引力的自我介绍',
            'user_template': '''请根据以下信息，生成一个{style}风格的{version}自我介绍。

## 信息内容：
{resume_content}

## 输出要求：
1. 仅输出自我介绍文本，不要包含任何额外内容
2. 自我介绍必须基于提供的信息，不要编造信息
3. 语言流畅，符合{style}风格
4. 时长控制在{version}对应的时间范围内
5. 突出个人优势和核心竞争力
6. 开头要有礼貌的问候语''',
            'user_template_generic': '''请生成一个{style}风格的{version}通用自我介绍。

## 输出要求：
1. 仅输出自我介绍文本，不要包含任何额外内容
2. 语言流畅，符合{style}风格
3. 时长控制在{version}对应的时间范围内
4. 突出个人优势和核心竞争力
5. 开头要有礼貌的问候语
6. 适用于大多数职业场景'''
        },
        
        # ===== 智能题库 =====
        'question_bank': {
            'system': '你是一位资深的技术面试官，擅长根据候选人简历生成针对性的面试题目',
            'user_template': '''请根据以下简历内容，生成{count}道高质量面试题，并严格按照JSON格式输出。

## 题目类型分布：
- 高频题（常见面试问题）：30%
- 深挖题（针对简历细节）：25%
- 专业技能题（技术相关）：25%
- 行为情景题（STAR法则）：20%

## 简历内容：
{resume_content}

## 自定义主题（可选）：
{custom_topic}

## 输出要求：
1. 严格按照以下JSON格式输出，不要包含任何额外文字或markdown标记
2. 每道题必须包含：question(问题)、answer(参考答案)、type(题目类型)、analysis(面试官意图)
3. 问题要有针对性，基于简历内容
4. 答案要详细专业

## 输出JSON格式示例：
{{"questions": [{{"question": "问题1", "answer": "答案1", "type": "高频题", "analysis": "意图1"}}, {{"question": "问题2", "answer": "答案2", "type": "深挖题", "analysis": "意图2"}}]}}

只输出上述格式的JSON，不要包含其他内容。'''
        },
        
        # ===== 模拟面试 =====
        'mock_interview': {
            'interviewer_system': '''你是一位{style}风格的面试官，正在进行一场{duration}分钟的模拟面试。

## 你的角色特点：
- 根据候选人的简历和回答提出针对性问题
- 评估候选人的专业能力、逻辑思维和表达能力
- 给出建设性的反馈

## 候选人简历：
{resume_content}''',
            
            'generate_question': '''基于候选人简历和之前的对话，生成下一个面试问题。
## 之前的对话：
{conversation_history}

## 要求：
1. 问题要有逻辑递进性
2. 可以是追问、深挖或转换话题
3. 只输出一个问题，不要有其他内容''',
            
            'start_interview': '''你是一位{style}风格的面试官，正在为候选人进行面试。请基于以下简历内容，生成第一个面试问题，要求：

1. 问题类型：高频必问题（如自我介绍、求职动机等）
2. 问题要与候选人的简历背景相关
3. 语言风格符合{style}特点
4. **所有对话内容必须使用中文**（包括问候语、问题内容等）
5. 仅输出JSON格式，包含id、content、type字段
6. 不要包含任何额外的文字或解释

简历内容：
{resume_content}''',

            'feedback_and_question': '''你是一位{style}风格的面试官，正在为候选人进行面试。请基于以下信息：

1. 简历内容：{resume_content}
2. 对话历史：{conversation_history}
3. 当前问题：{current_question}
4. 候选人回答：{answer}

请完成以下任务：

1. 生成对当前回答的反馈，要求：
   - 评价回答的质量、逻辑、深度
   - 指出优点和不足
   - 语言风格符合{style}
   - **反馈内容必须使用中文**

2. 生成下一个面试问题，要求：
   - 问题类型多样（简历深挖题、专业技能题、行为/情景题等）
   - 与候选人的简历和对话历史相关
   - 难度适中，符合面试流程
   - **问题内容必须使用中文**

输出格式要求：
{{"feedback": "对当前回答的反馈", "nextQuestion": {{"id": 数字id, "content": "下一个问题内容", "type": "问题类型"}}}}

**重要**：只输出JSON格式，所有文本内容使用中文，不要包含任何额外的文字或解释。在JSON字符串值内部不要使用双引号，如需引用请使用单引号。''',

            'evaluate_answer': '''评估候选人的回答质量。

## 问题：
{question}

## 候选人回答：
{answer}

## 输出JSON格式：
{{"score": 1-10分, "feedback": "评价", "follow_up": "可选的追问"}}''',
            
            'generate_report': '''你是一位专业的面试评估专家，正在为候选人生成面试报告。请基于以下信息：

1. 简历内容：{resume_content}
2. 面试风格：{style}
3. 面试时长：{duration}分钟
4. 问答记录：{question_answers}
5. 对话历史：{conversation_history}

请生成一份详细的面试报告，要求：

1. 包含以下评分项（0-100分）：
   - professionalScore：专业能力评分
   - logicScore：逻辑表达评分
   - confidenceScore：自信程度评分
   - matchScore：岗位匹配度评分

2. 逐题诊断，每个问题包含：
   - question：问题内容
   - answer：候选人回答
   - feedback：对该回答的评价
   - suggestion：改进建议

3. 优化建议，包含至少4条针对性建议

输出格式要求：
{{"professionalScore": 数字, "logicScore": 数字, "confidenceScore": 数字, "matchScore": 数字, "questionAnalysis": [{{"question": "问题内容", "answer": "候选人回答", "feedback": "评价", "suggestion": "改进建议"}}], "optimizationSuggestions": ["建议1", "建议2"]}}

**重要**：只输出JSON格式，不要包含任何额外的文字或解释。在JSON字符串值内部不要使用双引号，如需引用请使用单引号。'''
        },
        
        # ===== 面试策略 =====
        'strategy': {
            'analysis_system': '你是一位专业的面试策略分析师，擅长为候选人提供个性化的面试策略建议',
            'analysis_template': '''基于以下信息生成画像分析报告：

## 简历内容：
{resume_content}

## 用户背景信息：
{background_info}

## 优化方向：
{directions}

## 输出要求：
1. 严格按照JSON格式输出
2. 所有文本内容（title、content、tips）必须使用**中文**
3. 不要包含任何额外的文字或解释

## 输出JSON格式：
{{"sections": [{{"title": "章节标题", "content": "章节内容", "tips": ["建议1", "建议2"]}}]}}

只输出JSON格式，不要包含任何额外的文字或解释。''',
            
            'questions_system': '你是一位面试辅导专家，擅长生成高质量的反问问题',
            'questions_template': '''为候选人生成反问面试官的问题。

## 目标公司：{company}
## 目标岗位：{position}
## 问题类型：{question_types}

## 输出要求：
1. 严格按照JSON格式输出
2. 所有文本内容（content、type、explanation）必须使用**中文**

## 输出JSON格式：
{{"questions": [{{"content": "问题内容", "type": "问题类型", "explanation": "提问意图"}}]}}'''
        }
    },
    
    'en': {
        # ===== Resume Analysis =====
        'resume_analysis': {
            'system': 'You are a professional resume analyst specializing in evaluating technical resumes',
            'user_template': '''Please analyze the following resume and provide optimization suggestions in JSON format:

## Output Requirements:
1. **Output JSON string only**, no additional text or explanations
2. JSON must be strictly valid with double quotes and escaped special characters
3. Ensure all field types are correct
4. **IMPORTANT**: Do NOT use double quotes inside JSON string values, use single quotes for any quoted text within strings

## Required Fields:
- `score`: Integer, 0-100 overall score
- `diagnosis`: Array, each item contains `type`(warning/error/suggestion), `title`, `description`
- `keywords`: Array, at least 10 relevant technical keywords
- `starRewrite`: Array, each STAR contains `situation`, `task`, `action`, `result`
- `optimizedResume`: String, complete optimized resume in **beautiful Markdown format**

## Optimized Resume Format Requirements:
1. Use clear Markdown hierarchy
2. Use `#`, `##`, `###` for headings
3. Work experience in reverse chronological order
4. Highlight quantified results and key achievements

Resume Content:
{resume_content}'''
        },
        
        # ===== Self Introduction =====
        'self_intro': {
            'system': 'You are a professional self-introduction expert, skilled at creating natural, fluent, and engaging introductions',
            'user_template': '''Please generate a {style}-style {version} self-introduction based on the following information.

## Information:
{resume_content}

## Requirements:
1. Output only the self-introduction text, no additional content
2. Base it on the provided information, do not fabricate
3. Use fluent language in {style} style
4. Keep within the time range for {version}
5. Highlight personal strengths and core competencies
6. Start with a polite greeting''',
            'user_template_generic': '''Please generate a {style}-style {version} generic self-introduction.

## Requirements:
1. Output only the self-introduction text, no additional content
2. Use fluent language in {style} style
3. Keep within the time range for {version}
4. Highlight personal strengths and core competencies
5. Start with a polite greeting
6. Suitable for most professional scenarios'''
        },
        
        # ===== Question Bank =====
        'question_bank': {
            'system': 'You are a senior technical interviewer skilled at generating targeted interview questions based on candidate resumes',
            'user_template': '''Based on the following resume, generate {count} high-quality interview questions in JSON format.

## Question Type Distribution:
- High-frequency questions (common interview questions): 30%
- Deep-dive questions (resume-specific details): 25%
- Technical skill questions: 25%
- Behavioral scenario questions (STAR method): 20%

## Resume Content:
{resume_content}

## Custom Topic (optional):
{custom_topic}

## Output Requirements:
1. Strictly follow the JSON format below, no additional text or markdown
2. Each question must include: question, answer(reference answer), type(question type), analysis(interviewer intent)
3. Questions should be targeted based on resume
4. Answers should be detailed and professional

## Output JSON Format Example:
{{"questions": [{{"question": "Question 1", "answer": "Answer 1", "type": "High-frequency", "analysis": "Intent 1"}}, {{"question": "Question 2", "answer": "Answer 2", "type": "Deep-dive", "analysis": "Intent 2"}}]}}

Output only the above JSON format, no other content.'''
        },
        
        # ===== Mock Interview =====
        'mock_interview': {
            'interviewer_system': '''You are a {style}-style interviewer conducting a {duration}-minute mock interview.

## Your Character Traits:
- Ask targeted questions based on the candidate's resume and responses
- Evaluate professional skills, logical thinking, and communication
- Provide constructive feedback

## Candidate Resume:
{resume_content}''',
            
            'generate_question': '''Based on the candidate's resume and previous conversation, generate the next interview question.

## Previous Conversation:
{conversation_history}

## Requirements:
1. Questions should have logical progression
2. Can be follow-up, deep-dive, or topic change
3. Output only one question, nothing else''',
            
            'start_interview': '''You are a {style}-style interviewer conducting an interview. Based on the resume below, generate the first interview question.

Requirements:
1. Question type: Common opening question (e.g., self-introduction, motivation)
2. Must be relevant to candidate's background
3. Language style matches {style}
4. **All conversation content must be in English** (including greetings, questions, etc.)
5. Output JSON format only, including id, content, type fields
6. No additional text or explanations

Resume Content:
{resume_content}''',

            'feedback_and_question': '''You are a {style}-style interviewer. Based on:

1. Resume: {resume_content}
2. History: {conversation_history}
3. Current Question: {current_question}
4. Candidate Answer: {answer}

Please complete:

1. Generate feedback for the current answer:
   - Evaluate quality, logic, depth
   - Point out pros and cons
   - Style matches {style}
   - **Feedback content must be in English**

2. Generate the next interview question:
   - Diverse types (deep-dive, technical, behavioral)
   - Relevant to resume and history
   - Appropriate difficulty
   - **Question content must be in English**

Output Format:
{{"feedback": "Feedback content", "nextQuestion": {{"id": number, "content": "Next question content", "type": "Question type"}}}}

**IMPORTANT**: Output JSON format only. All text content must be in English. Do NOT use double quotes inside JSON string values, use single quotes instead.''',

            'evaluate_answer': '''Evaluate the candidate's answer quality.

## Question:
{question}

## Candidate's Answer:
{answer}

## Output JSON format:
{{"score": 1-10, "feedback": "evaluation", "follow_up": "optional follow-up question"}}''',
            
            'generate_report': '''Generate an interview review report based on:

1. Resume: {resume_content}
2. Style: {style}
3. Duration: {duration} minutes
4. Q&A Log: {question_answers}
5. History: {conversation_history}

Generate a detailed report including:

1. Scores (0-100):
   - professionalScore
   - logicScore
   - confidenceScore
   - matchScore

2. Question Analysis (for each question):
   - question
   - answer
   - feedback
   - suggestion

3. Optimization Suggestions (at least 4)

Output Format:
{{"professionalScore": number, "logicScore": number, "confidenceScore": number, "matchScore": number, "questionAnalysis": [{{"question": "content", "answer": "content", "feedback": "content", "suggestion": "content"}}], "optimizationSuggestions": ["suggestion1", "suggestion2"]}}

**IMPORTANT**: Output JSON format only. Do NOT use double quotes inside JSON string values, use single quotes instead.'''
        },
        
        # ===== Interview Strategy =====
        'strategy': {
            'analysis_system': 'You are a professional interview strategy analyst, skilled at providing personalized interview strategy advice',
            'analysis_template': '''Generate a profile analysis report based on the following information:

## Resume Content:
{resume_content}

## User Background:
{background_info}

## Optimization Directions:
{directions}

## Output Requirements:
1. Strictly follow JSON format
2. All text content (title, content, tips) must be in **English**
3. No additional text or explanations

## Output JSON format:
{{"sections": [{{"title": "Section Title", "content": "Section Content", "tips": ["Tip 1", "Tip 2"]}}]}}

Output JSON format only, no additional text or explanations.''',
            
            'questions_system': 'You are an interview coaching expert skilled at generating high-quality questions to ask interviewers',
            'questions_template': '''Generate questions for the candidate to ask the interviewer.

## Target Company: {company}
## Target Position: {position}
## Question Types: {question_types}

## Output Requirements:
1. Strictly follow JSON format
2. All text content (content, type, explanation) must be in **English**

## Output JSON format:
{{"questions": [{{"content": "Question content", "type": "Question type", "explanation": "Purpose of asking"}}]}}'''
        }
    }
}


def get_prompt(prompt_key, locale='zh', sub_key=None):
    """
    获取指定语言的prompt模板
    
    Args:
        prompt_key: 主键名，如 'resume_analysis', 'self_intro'
        locale: 语言代码，'zh' 或 'en'
        sub_key: 子键名（可选），如 'system', 'user_template'
    
    Returns:
        dict 或 str: 完整的prompt配置或特定子项
    """
    # 确保locale有效
    if locale not in PROMPTS:
        locale = 'zh'
    
    # 获取prompt配置
    prompts = PROMPTS[locale]
    if prompt_key not in prompts:
        # 如果指定语言没有这个模板，回退到中文
        prompts = PROMPTS['zh']
    
    prompt_config = prompts.get(prompt_key, {})
    
    # 如果指定了子键，返回子项
    if sub_key:
        return prompt_config.get(sub_key, '')
    
    return prompt_config


def get_system_prompt(prompt_key, locale='zh', sub_key='system'):
    """获取系统提示词
    
    Args:
        prompt_key: 主键名
        locale: 语言代码
        sub_key: 系统提示词子键名，默认'system'
    """
    return get_prompt(prompt_key, locale, sub_key)


def get_user_prompt(prompt_key, locale='zh', template_key='user_template', **kwargs):
    """
    获取用户提示词并填充变量
    
    Args:
        prompt_key: 主键名
        locale: 语言代码
        template_key: 模板子键名，默认 'user_template'
        **kwargs: 模板变量
    
    Returns:
        str: 填充后的用户提示词
    """
    template = get_prompt(prompt_key, locale, template_key)
    if template and kwargs:
        try:
            return template.format(**kwargs)
        except KeyError as e:
            print(f"[Prompt Templates] Missing template variable: {e}")
            return template
    return template
