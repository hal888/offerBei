# Helper function for batch generation
def generate_questions_batch(client, resume_content, topic, batch_size, batch_idx, num_batches):
    """生成一批题目"""
    import json
    import re
    
    print(f"[DEBUG] 第{batch_idx + 1}/{num_batches}批，生成{batch_size}题")
    
    # 生成prompt
    if topic:
        batch_prompt = f"""
        请基于以下简历内容和指定话题，生成{batch_size}个与候选人背景和话题紧密相关的面试问题，涵盖高频必问题、简历深挖题、专业技能题和行为/情景题等类型。
        
        ## 指定话题：
        {topic}
        
        ## 简历内容：
        {resume_content}
        
        ## 输出要求：
        1. 仅输出JSON字符串，不要包含任何额外的文字、解释或说明
        2. JSON格式必须严格有效，使用双引号，转义所有特殊字符
        3. 每个问题必须包含：id, content, type, answer, analysis
        4. 问题必须与候选人简历和话题紧密相关
        
        ## 输出格式：
        {{"questions":[{{"id":1,"content":"问题内容","type":"题目类型","answer":"参考答案","analysis":"分析"}}]}}
        """
    else:
        batch_prompt = f"""
        请基于以下简历内容，生成{batch_size}个与候选人背景相关的面试问题。
        
        ## 简历内容：
        {resume_content}
        
        ## 输出要求：
        1. 仅输出JSON字符串
        2. 每个问题必须包含：id, content, type, answer, analysis
        
        ## 输出格式：
        {{"questions":[{{"id":1,"content":"问题内容","type":"题目类型","answer":"参考答案","analysis":"分析"}}]}}
        """
    
    # 计算max_tokens
    batch_max_tokens = min(int((500 + 600 * batch_size) * 1.2), 8192)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位专业的面试问题生成专家，擅长根据候选人的简历内容生成相关的面试问题"},
                {"role": "user", "content": batch_prompt}
            ],
            temperature=0.7,
            max_tokens=batch_max_tokens
        )
        
        api_result = response.choices[0].message.content
        
        # 清理和解析JSON
        cleaned_response = api_result
        if cleaned_response.startswith('```json') or cleaned_response.startswith('```'):
            cleaned_response = cleaned_response.split('\n', 1)[1]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response.rsplit('\n', 1)[0]
        
        start_idx = cleaned_response.find('{')
        end_idx = cleaned_response.rfind('}') + 1
        if start_idx == -1 or end_idx <= start_idx:
            print(f"[批次{batch_idx + 1}] JSON结构无效")
            return []
        
        json_content = cleaned_response[start_idx:end_idx]
        json_content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', json_content)
        
        batch_result = json.loads(json_content)
        batch_questions = batch_result.get("questions", [])
        print(f"[DEBUG] 批次{batch_idx + 1}成功: {len(batch_questions)}题")
        return batch_questions
        
    except Exception as e:
        print(f"[批次{batch_idx + 1}] 失败: {e}")
        return []
