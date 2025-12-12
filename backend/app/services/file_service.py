import os
import uuid
import re
from config import RESUME_CONFIG

def clean_text(content):
    """
    高级文本清理，保留结构信息
    """
    # 1. 移除多余空行（保留最多2个连续空行）
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 2. 处理特殊字符和乱码
    # 保留中文字符、英文字母、数字和常见标点
    content = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s,.!?;:\'"()\[\]{}\-_+=~`@#$%^&*，。！？；：‘’“”（）【】{}、|\\/]', '', content)
    
    # 3. 标准化空格
    content = re.sub(r'\s+', ' ', content).replace(' \n', '\n').replace('\n ', '\n')
    
    # 4. 修复断词（如"Py\nMuPDF" → "PyMuPDF"）
    content = re.sub(r'(\w)\n(\w)', r'\1\2', content)
    
    return content.strip()

def is_table_block(block):
    """
    检测文本块是否为表格
    """
    # 基于块的特征判断是否为表格
    lines = block.get("lines", [])
    if len(lines) < 2:  # 至少2行才可能是表格
        return False
    
    # 检查每行的词数是否相近（表格特征）
    word_counts = [len(line.get("spans", [])) for line in lines]
    if max(word_counts) - min(word_counts) > 2:
        return False
    
    return True

def extract_table_from_block(block):
    """
    从文本块中提取表格内容
    """
    table_rows = []
    
    for line in block["lines"]:
        row = [span["text"] for span in line["spans"]]
        table_rows.append("\t".join(row))  # 使用制表符分隔列
    
    return "\n".join(table_rows)

def extract_text_with_layout(page):
    """
    使用布局模式提取文本，保留文档结构和正确的阅读顺序
    """
    # 使用layout模式提取详细布局信息
    text_dict = page.get_text("dict")
    
    # 提取所有文本块，并按y坐标（从上到下）排序
    text_blocks = []
    for block in text_dict["blocks"]:
        if block["type"] == 0:  # 文本块
            if block.get("bbox"):
                # 获取文本块的y坐标（顶部）
                y_top = block["bbox"][1]
                text_blocks.append((y_top, block))
    
    # 按y坐标排序，确保从上到下读取
    text_blocks.sort(key=lambda x: x[0])
    
    # 按块、行、词的顺序重组文本
    content = []
    
    for y_top, block in text_blocks:
        # 检查是否为表格
        if is_table_block(block):
            table_content = extract_table_from_block(block)
            content.append(table_content)
        else:
            # 普通文本块，按行处理
            block_text = []
            for line in block["lines"]:
                line_text = "".join([span["text"] for span in line["spans"]])
                block_text.append(line_text)
            content.append("\n".join(block_text))
    
    # 对内容进行结构化重组，优化简历格式
    restructured_content = restructure_resume_content("\n\n".join(content))
    
    return restructured_content

def restructure_resume_content(content):
    """
    对简历内容进行结构化重组，确保个人信息在最前面
    """
    # 定义简历各部分的关键词
    personal_info_keywords = ["男|女", "年龄", "岁", "联系方式", "电话", "邮箱", "求职意向", "期望薪资", "期望城市"]
    work_exp_keywords = ["工作经历", "职业经历", "任职经历", "工作经验"]
    education_keywords = ["教育背景", "学历", "学习经历", "毕业院校"]
    skills_keywords = ["专业技能", "技能", "技术栈", "能力"]
    projects_keywords = ["项目经历", "项目经验", "项目", "作品"]
    advantage_keywords = ["个人优势", "优势", "特长", "亮点"]
    
    # 首先处理页面分割标记，移除或整合页面标记
    # 移除页面标记，只保留内容
    import re
    content = re.sub(r'--- 第\d+页 ---', '', content)
    # 清理可能的空白字符
    content = content.strip()
    
    # 预处理：按行分割内容
    lines = content.split("\n")
    
    # 1. 首先提取个人信息（通常在简历最顶部）
    personal_info_lines = []
    remaining_lines = []
    found_personal = False
    personal_end_markers = ["个人优势", "专业技能", "工作经历", "教育背景", "项目经历"]
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检查是否包含个人信息关键词
        has_personal_keyword = any(keyword in line for keyword in personal_info_keywords)
        has_name = len(line) < 200 and ("姓名" in line or (len(line) < 50 and any(c.isalpha() for c in line)))
        has_contact = "@" in line or "电话" in line or "手机" in line or re.search(r'1[3-9]\d{9}', line)
        
        if has_personal_keyword or has_name or has_contact:
            personal_info_lines.append(line)
            found_personal = True
        elif found_personal and any(marker in line for marker in personal_end_markers):
            # 找到个人信息结束标记，添加标记行到剩余行
            remaining_lines.append(line)
            found_personal = False
        elif found_personal:
            # 仍然是个人信息的一部分
            personal_info_lines.append(line)
        else:
            # 非个人信息行
            remaining_lines.append(line)
    
    # 合并个人信息行
    personal_info = [" ".join(personal_info_lines)] if personal_info_lines else []
    
    # 2. 处理剩余内容，按标记分割为不同部分
    remaining_content = "\n".join(remaining_lines)
    
    # 定义部分顺序和标记
    sections = [
        ("advantages", "个人优势", advantage_keywords),
        ("skills", "专业技能", skills_keywords),
        ("work_exp", "工作经历", work_exp_keywords),
        ("projects", "项目经历", projects_keywords),
        ("education", "教育背景", education_keywords)
    ]
    
    # 初始化各部分内容
    advantage_content = ""
    skills_content = ""
    work_exp_content = ""
    projects_content = ""
    education_content = ""
    
    # 按顺序提取各部分内容
    current_content = remaining_content
    
    for section_name, section_title, section_keywords in sections:
        # 查找当前部分的开始位置
        start_pos = -1
        for keyword in section_keywords:
            pos = current_content.find(keyword)
            if pos != -1 and (start_pos == -1 or pos < start_pos):
                start_pos = pos
        
        if start_pos != -1:
            # 提取当前部分的内容
            section_content = current_content[start_pos:]
            
            # 查找下一部分的开始位置，作为当前部分的结束
            end_pos = len(section_content)
            for next_section in sections[sections.index((section_name, section_title, section_keywords)) + 1:]:
                for next_keyword in next_section[2]:
                    pos = section_content.find(next_keyword)
                    if pos != -1 and pos < end_pos:
                        end_pos = pos
            
            # 提取当前部分的完整内容
            section_content = section_content[:end_pos].strip()
            
            # 保存到对应的变量
            if section_name == "advantages":
                advantage_content = section_content
            elif section_name == "skills":
                skills_content = section_content
            elif section_name == "work_exp":
                work_exp_content = section_content
            elif section_name == "projects":
                projects_content = section_content
            elif section_name == "education":
                education_content = section_content
            
            # 更新当前内容，移除已处理的部分
            current_content = current_content[:start_pos].strip()
    
    # 构建结构化内容
    restructured = []
    
    # 1. 个人信息（确保在最前面）
    if personal_info:
        restructured.extend(personal_info)
    
    # 2. 个人优势
    if advantage_content:
        restructured.append(advantage_content)
    
    # 3. 专业技能
    if skills_content:
        restructured.append(skills_content)
    
    # 4. 工作经历
    if work_exp_content:
        restructured.append(work_exp_content)
    
    # 5. 项目经历
    if projects_content:
        restructured.append(projects_content)
    
    # 6. 教育背景
    if education_content:
        restructured.append(education_content)
    
    # 构建最终的结构化内容
    return "\n\n".join(restructured)

def extract_text_with_ocr(page):
    """
    使用OCR提取扫描型PDF文本
    """
    try:
        import pytesseract
        from PIL import Image
        import io
        
        # 将PDF页面转换为图像
        pix = page.get_pixmap(dpi=300)  # 高DPI确保OCR准确性
        img = Image.open(io.BytesIO(pix.tobytes()))
        
        # 执行OCR
        text = pytesseract.image_to_string(img, lang="chi_sim+eng")  # 支持中英文
        
        return text
    except Exception as e:
        print(f"OCR提取失败: {e}")
        # 降级为基本文本提取
        return page.get_text("text")

def read_optimized_pdf(file_path):
    """
    优化的PDF读取函数，支持复杂格式
    """
    import fitz
    content = ""
    doc = fitz.open(file_path)
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # 检查页面是否包含文本
        text_info = page.get_text("dict")
        has_text = any(block["type"] == 0 for block in text_info["blocks"])
        
        if has_text:
            # 文本型PDF：使用布局感知提取
            page_content = extract_text_with_layout(page)
        else:
            # 扫描型PDF：使用OCR
            page_content = extract_text_with_ocr(page)
        
        content += f"--- 第{page_num+1}页 ---\n{page_content}\n\n"
    
    doc.close()
    return content

def read_file_content(file_path, file_ext):
    """
    优化的文件内容读取函数，支持PDF和DOCX格式
    
    Args:
        file_path: 文件路径
        file_ext: 文件扩展名
        
    Returns:
        str: 文件内容
    """
    content = ""
    
    try:
        if file_ext == 'pdf':
            content = read_optimized_pdf(file_path)
        elif file_ext == 'docx':
            from docx import Document
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
        else:
            # 处理纯文本文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # 应用高级文本清理
        content = clean_text(content)
        
    except Exception as e:
        print(f"Error reading file: {e}")
        import traceback
        traceback.print_exc()  # 记录详细错误信息
        content = ""
    
    return content

def save_resume(file_content, resume_type='original', resume_id=None):
    """
    保存简历内容到文件
    
    Args:
        file_content: 简历内容
        resume_type: 简历类型（original/optimized）
        resume_id: 可选，指定resumeId，否则自动生成
        
    Returns:
        str: 生成或指定的resumeId
    """
    # 如果没有指定resumeId，则生成唯一的resumeId
    if not resume_id:
        resume_id = uuid.uuid4().hex[:8]
    
    # 根据简历类型获取对应的子路径
    sub_path = RESUME_CONFIG['original_path'] if resume_type == 'original' else RESUME_CONFIG['optimized_path']
    
    # 构建完整的保存路径
    base_path = RESUME_CONFIG['base_path']
    full_path = os.path.join(base_path, sub_path)
    
    # 确保目录存在
    os.makedirs(full_path, exist_ok=True)
    
    # 构建文件路径
    file_path = os.path.join(full_path, f'{resume_id}.txt')
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    return resume_id

def get_resume_content(resume_id, resume_type='optimized'):
    """
    获取保存的简历内容
    
    Args:
        resume_id: 简历ID
        resume_type: 简历类型（original/optimized）
        
    Returns:
        str: 简历内容
    """
    # 根据简历类型获取对应的子路径
    sub_path = RESUME_CONFIG['original_path'] if resume_type == 'original' else RESUME_CONFIG['optimized_path']
    
    # 构建完整的文件路径
    file_path = os.path.join(RESUME_CONFIG['base_path'], sub_path, f'{resume_id}.txt')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # 如果是默认resume_id为1且文件不存在，返回一个示例简历内容
        if resume_id == '1':
            return "# 示例简历\n\n## 个人信息\n张三 | 前端开发工程师\n\n## 工作经历\n2020-至今 某互联网公司 前端开发工程师\n- 负责公司核心产品的前端开发\n- 熟练使用Vue、React等前端框架\n- 参与过多个大型项目的开发\n\n## 教育背景\n2016-2020 某大学 计算机科学与技术 本科\n\n## 技能\n- 前端框架：Vue、React、Angular\n- 编程语言：JavaScript、TypeScript、HTML、CSS\n- 其他技能：Git、Webpack、Node.js"
        return ""
