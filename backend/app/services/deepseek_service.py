from openai import OpenAI
from config import DEEPSEEK_CONFIG
from ..utils.prompt_templates import get_system_prompt, get_user_prompt

# 配置DeepSeek API客户端
client = OpenAI(
    api_key=DEEPSEEK_CONFIG["api_key"],
    base_url=DEEPSEEK_CONFIG["base_url"]
)

def generate_self_intro(resume_content, version, style, locale='zh'):
    """
    根据简历内容生成自我介绍
    
    Args:
        resume_content: 简历内容
        version: 版本（30秒电梯演讲版/3分钟标准版/5分钟深度版）
        style: 风格（正式/活泼/专业/亲切）
        locale: 语言代码 ('zh' 或 'en')
        
    Returns:
        str: 生成的自我介绍文本
    """
    # 获取系统提示词
    system_prompt = get_system_prompt('self_intro', locale)
    
    # 获取用户提示词模板
    if resume_content:
        user_prompt = get_user_prompt(
            'self_intro', 
            locale, 
            'user_template',
            resume_content=resume_content,
            version=version,
            style=style
        )
    else:
        # 如果没有任何信息，使用通用模板
        user_prompt = get_user_prompt(
            'self_intro',
            locale,
            'user_template_generic',
            version=version,
            style=style
        )
    
    response = client.chat.completions.create(
        model=DEEPSEEK_CONFIG["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=8192
    )
    
    return response.choices[0].message.content.strip()

def analyze_resume(resume_content, locale='zh'):
    """
    分析简历内容，生成优化建议
    
    Args:
        resume_content: 原始简历内容
        locale: 语言代码 ('zh' 或 'en')
        
    Returns:
        str: DeepSeek API返回的分析结果
    """
    # 获取系统提示词
    system_prompt = get_system_prompt('resume_analysis', locale)
    
    # 获取用户提示词
    user_prompt = get_user_prompt(
        'resume_analysis',
        locale,
        'user_template',
        resume_content=resume_content
    )
    
    response = client.chat.completions.create(
        model=DEEPSEEK_CONFIG["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=8192
    )
    
    return response.choices[0].message.content
