import json
import re

def parse_resume_result(content):
    """
    解析DeepSeek返回的简历分析结果，处理JSON格式响应
    
    Args:
        content: DeepSeek返回的原始响应内容
        
    Returns:
        dict: 解析后的结果
    """
    # 默认结果结构
    result = {
        "score": 0,
        "diagnosis": [],
        "keywords": [],
        "starRewrite": [],
        "optimizedResume": ""
    }
    
    # content内容写入文件
    # with open('response.txt', 'w', encoding='utf-8') as f:
    #     f.write(content)
    
    # print("=== 开始JSON解析 ===")
    # print(f"原始响应长度：{len(content)}字符")
    # print(f"响应内容：{content}")
    
    try:
        # 1. 清理可能的额外内容，只保留JSON部分
        # 查找JSON的起始和结束位置
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        
        if start_idx == -1:
            print("❌ 未找到JSON起始标记 '{'")
            return result
        
        if end_idx <= start_idx:
            print(f"❌ JSON结束位置无效：start={start_idx}, end={end_idx}")
            return result
        
        # 提取JSON内容
        json_content = content[start_idx:end_idx]
        print(f"✓ 提取JSON内容：{len(json_content)}字符")
        print(f"✓ JSON前50字符：{json_content[:50]}...")
        
        # 2. 清理JSON中的可能问题
        # 移除可能的Markdown代码块标记
        json_content = json_content.replace('```json', '').replace('```', '')
        
        # 移除多余的换行符和空格
        json_content = ' '.join(json_content.split())
        
        # 3. 修复常见JSON格式问题
        # 修复尾随逗号（在}或]之前的逗号）
        json_content = re.sub(r',\s*([}\]])', r' \1', json_content)
        
        # 移除JSON中的注释（如果有）
        json_content = re.sub(r'//.*?(?=\\n|$)', '', json_content)
        json_content = re.sub(r'/\*.*?\*/', '', json_content, flags=re.DOTALL)
        
        # 修复嵌套引号问题 - 使用更简单安全的方法
        # 策略1: 替换常见的英文示例中的嵌套引号 (e.g., "xxx") -> (e.g., 'xxx')
        json_content = re.sub(r'\(e\.g\.,?\s*"([^"]{1,100})"', r"(e.g., '\1'", json_content)
        json_content = re.sub(r'\(i\.e\.,?\s*"([^"]{1,100})"', r"(i.e., '\1'", json_content)
        
        # 策略2: 替换 "xxx" 这种在描述中的引用 -> 'xxx'
        # 匹配模式: 单词后跟空格和引号开始的短语
        json_content = re.sub(r'(\w)\s+"([^"]{1,50})"\s*([,\.\)])', r"\1 '\2'\3", json_content)
        
        # 策略3: 修复英文所有格撇号被写成双引号的问题 (candidate"s -> candidate's)
        json_content = re.sub(r'(\w)"s\b', r"\1's", json_content)
        json_content = re.sub(r'(\w)"t\b', r"\1't", json_content)  # don"t -> don't
        json_content = re.sub(r'(\w)"re\b', r"\1're", json_content)  # you"re -> you're
        json_content = re.sub(r'(\w)"ll\b', r"\1'll", json_content)  # you"ll -> you'll
        json_content = re.sub(r'(\w)"ve\b', r"\1've", json_content)  # you"ve -> you've
        
        # 移除可能的控制字符，但保留Unicode字符
        json_content = re.sub(r'[\x00-\x1f\x7f]', '', json_content)  # 只移除控制字符
        
        # print(f"✓ 清理后JSON：{json_content[:100]}...")
        
        # 3. 解析JSON
        json_result = json.loads(json_content)
        # print("✓ JSON解析成功！")
        
        # 4. 验证并提取所需字段
        if not isinstance(json_result, dict):
            print("❌ JSON结果不是对象类型")
            return result
        
        # print(f"✓ 提取到字段：{list(json_result.keys())}")
        
        # 提取评分
        if 'score' in json_result and isinstance(json_result['score'], (int, float)):
            result['score'] = int(json_result['score'])
            # print(f"✓ 提取评分：{result['score']}")
        
        # 提取诊断意见
        if 'diagnosis' in json_result and isinstance(json_result['diagnosis'], list):
            # 支持中英文诊断类型
            valid_types_zh = ['警告', '错误', '建议']
            valid_types_en = ['warning', 'error', 'suggestion']
            valid_types = valid_types_zh + valid_types_en
            for item in json_result['diagnosis']:
                if isinstance(item, dict) and \
                   all(k in item for k in ['type', 'title', 'description']) and \
                   item['type'] in valid_types:
                    result['diagnosis'].append({
                        "type": item['type'],
                        "title": item['title'],
                        "description": item['description']
                    })
            # print(f"✓ 提取诊断意见：{len(result['diagnosis'])}条")
        
        # 提取关键词
        if 'keywords' in json_result and isinstance(json_result['keywords'], list):
            result['keywords'] = [k.strip() for k in json_result['keywords'] if isinstance(k, str) and k.strip()]
            # print(f"✓ 提取关键词：{len(result['keywords'])}个")
        
        # 提取STAR法则重写
        if 'starRewrite' in json_result and isinstance(json_result['starRewrite'], list):
            for item in json_result['starRewrite']:
                if isinstance(item, dict):
                    result['starRewrite'].append({
                        "situation": item.get('situation', '').strip(),
                        "task": item.get('task', '').strip(),
                        "action": item.get('action', '').strip(),
                        "result": item.get('result', '').strip()
                    })
            # print(f"✓ 提取STAR重写：{len(result['starRewrite'])}条")
        
        # 提取优化后简历
        if 'optimizedResume' in json_result and isinstance(json_result['optimizedResume'], str):
            result['optimizedResume'] = json_result['optimizedResume'].strip()
            # print(f"✓ 提取优化后简历：{len(result['optimizedResume'])}字符")
        
        # print("=== JSON解析完成 ===")
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误：{e}")
        print(f"❌ 错误位置：行{e.lineno}，列{e.colno}")
        print(f"❌ 错误片段：{json_content[max(0, e.pos-20):e.pos+20]}")
    except Exception as e:
        print(f"❌ JSON处理异常：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("=== JSON解析失败 ===")
    return result
