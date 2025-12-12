from openai import OpenAI
from config import DEEPSEEK_CONFIG

# 配置DeepSeek API客户端
client = OpenAI(
    api_key=DEEPSEEK_CONFIG["api_key"],
    base_url=DEEPSEEK_CONFIG["base_url"]
)

def generate_self_intro(resume_content, version, style):
    """
    根据简历内容生成自我介绍
    
    Args:
        resume_content: 简历内容
        version: 版本（30秒电梯演讲版/3分钟标准版/5分钟深度版）
        style: 风格（正式/活泼/专业/亲切）
        
    Returns:
        str: 生成的自我介绍文本
    """
    if resume_content:
        prompt = f"""
        请根据以下信息，生成一个{style}风格的{version}自我介绍。
        
        ## 信息内容：
        {resume_content}
        
        ## 输出要求：
        1. 仅输出自我介绍文本，不要包含任何额外内容
        2. 自我介绍必须基于提供的信息，不要编造信息
        3. 语言流畅，符合{style}风格
        4. 时长控制在{version}对应的时间范围内
        5. 突出个人优势和核心竞争力
        6. 开头要有礼貌的问候语
        """
    else:
        # 如果没有任何信息，生成通用自我介绍
        prompt = f"""
        请生成一个{style}风格的{version}通用自我介绍。
        
        ## 输出要求：
        1. 仅输出自我介绍文本，不要包含任何额外内容
        2. 语言流畅，符合{style}风格
        3. 时长控制在{version}对应的时间范围内
        4. 突出个人优势和核心竞争力
        5. 开头要有礼貌的问候语
        6. 适用于大多数职业场景
        """
    
    response = client.chat.completions.create(
        model=DEEPSEEK_CONFIG["model"],
        messages=[
            {"role": "system", "content": "你是一位专业的自我介绍生成专家，擅长生成自然、流畅、有吸引力的自我介绍"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content.strip()

def analyze_resume(resume_content):
    """
    分析简历内容，生成优化建议
    
    Args:
        resume_content: 原始简历内容
        
    Returns:
        str: DeepSeek API返回的分析结果
    """
    prompt = f"""
    请对以下简历内容进行全面分析和优化，并严格按照以下要求输出JSON格式结果：
    
    ## 输出要求：
    1. **仅输出JSON字符串**，不要包含任何额外的文字、解释或说明
    2. JSON格式必须严格有效，使用双引号，转义所有特殊字符（如换行符\n）
    3. 确保所有字段类型正确
    
    ## 必须包含的字段：
    - `score`: 整数，0-100分的综合评分
    - `diagnosis`: 数组，每条诊断包含`type`(警告/错误/建议)、`title`、`description`
    - `keywords`: 数组，至少10个与技术岗位相关的关键词
    - `starRewrite`: 数组，每条STAR包含`situation`、`task`、`action`、`result`
    - `optimizedResume`: 字符串，完整的优化后简历内容，**必须使用美观的Markdown格式**
    
    ## 优化后简历（optimizedResume）的格式要求：
    1. 使用清晰的Markdown层级结构
    2. 标题使用`#`、`##`、`###`等标记，明确区分不同章节
    3. 个人信息部分：姓名、联系方式、邮箱等信息清晰展示
    4. 教育经历：按时间倒序排列，包含学校、专业、学位、时间
    5. 工作经历：按时间倒序排列，每个职位包含公司、职位、时间
       - 使用项目符号或数字列表清晰展示职责和成就
       - 重点突出量化结果和关键成就
    6. 技能部分：分类展示（如技术技能、软技能），使用合适的格式（如列表、表格）
    7. 项目经验：清晰描述项目背景、职责、技术栈和成果
    8. 保持适当的留白和行距，提高可读性
    9. 使用简洁、专业的语言
    
    ## 示例输出格式：
    ```json
    {{"score":85,"diagnosis":[{{"type":"警告","title":"缺乏量化结果","description":"工作经历中缺乏具体的数据支撑"}}],"keywords":["JavaScript","Vue"],"starRewrite":[{{"situation":"在电商项目中","task":"负责前端开发","action":"使用Vue框架开发","result":"提升了页面性能"}}],"optimizedResume":"# 张三\n\n## 个人信息\n- 职位：前端开发工程师\n- 邮箱：zhangsan@example.com\n- 电话：13800138000\n\n## 教育经历\n### 北京大学 计算机科学与技术 硕士\n2018.09 - 2021.06\n\n## 工作经历\n### 科技有限公司 前端开发工程师\n2021.07 - 至今\n- 使用Vue.js开发电商平台前端，提升页面加载速度30%\n- 优化移动端适配，用户满意度提升25%\n\n## 技能栈\n- **前端框架**：Vue.js、React\n- **开发语言**：JavaScript、TypeScript\n- **工具**：Webpack、Git\n\n## 项目经验\n### 电商平台重构\n- 负责前端架构设计和核心模块开发\n- 技术栈：Vue 3 + TypeScript + Vite\n- 成果：页面加载时间从3s减少到1s\n"}}
    ```
    
    简历内容：
    {resume_content}
    """
    
    response = client.chat.completions.create(
        model=DEEPSEEK_CONFIG["model"],
        messages=[
            {"role": "system", "content": "你是一位专业的简历分析专家，擅长评估技术岗位的简历"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=8192
    )
    
    return response.choices[0].message.content
