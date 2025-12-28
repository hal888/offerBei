import os
import uuid
from config import RESUME_CONFIG
import pdfplumber

def read_file_content(file_path, file_ext):
    """
    读取文件内容，支持PDF和DOCX格式
    
    Args:
        file_path: 文件路径
        file_ext: 文件扩展名
        
    Returns:
        str: 文件内容
    """

    """解析带复杂表格的PDF，保留表格行列结构"""
    content = ""
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            
            # 提取普通文本（保留段落格式）
            text = page.extract_text()
            content += text + "\n\n"
    
    # try:
    #     if file_ext == 'pdf':
    #         # 使用PyMuPDF替代PyPDF2，优化PDF文本提取
    #         import fitz  # PyMuPDF的导入名是fitz
    #         doc = fitz.open(file_path)
    #         for page_num in range(doc.page_count):
    #             page = doc.load_page(page_num)
    #             # 提取文本，使用空格分隔避免格式错乱
    #             page_text = page.get_text("text") or ""
    #             # 清理文本，移除多余的空行和空格
    #             page_text = '\n'.join([line.strip() for line in page_text.split('\n') if line.strip()])
    #             content += page_text + "\n\n"
    #         doc.close()
    #     elif file_ext == 'docx':
    #         from docx import Document
    #         doc = Document(file_path)
    #         for paragraph in doc.paragraphs:
    #             content += paragraph.text + "\n"
    #     else:
    #         # 处理纯文本文件
    #         with open(file_path, 'r', encoding='utf-8') as f:
    # #             content = f.read()
    # except Exception as e:
    #     print(f"Error reading file: {e}")
    #     content = ""
    
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
