from flask import Blueprint, request, jsonify
from ..services.deepseek_service import client
from ..services.file_service import get_resume_content
from ..models import db, User, InterviewStrategy
from ..utils.jwt_utils import auth_required
from ..utils.messages import get_message
from ..utils.prompt_templates import get_system_prompt, get_user_prompt
import json
import uuid

# 创建蓝图
bp = Blueprint('strategy', __name__, url_prefix='/api/strategy')

@bp.route('/analysis', methods=['POST'])
@auth_required
def analysis():
    """生成面试策略及画像分析API"""
    data = request.get_json()
    background_info = data.get('backgroundInfo', '')
    directions = data.get('directions', [])
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
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
    print(f"[API LOG] /api/strategy/analysis - Request received: userId={user_id}, resumeId={resume_id}, backgroundInfo={background_info[:50]}...")
    
    # 获取简历内容
    resume_content = get_resume_content(resume_id, 'optimized')
    
    # 构建用户Prompt
    user_prompt = get_user_prompt(
        'strategy',
        locale,
        'analysis_template',
        resume_content=resume_content,
        background_info=background_info,
        directions=json.dumps(directions) if directions else "（无具体方向）"
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": get_system_prompt('strategy', locale, 'analysis_system')},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=8192
        )
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        try:
            # 清理可能的额外内容，只保留JSON部分
            start_idx = api_result.find('{')
            end_idx = api_result.rfind('}') + 1
            if start_idx == -1 or end_idx <= start_idx:
                raise ValueError("未找到有效的JSON结构")
            
            json_content = api_result[start_idx:end_idx]
            
            # 清理无效控制字符
            import re
            # 移除所有控制字符，除了制表符、换行符和回车符
            json_content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', json_content)
            # 清理JSON字符串中的中文引号
            json_content = re.sub(r'[“”]', '"', json_content)
            json_content = re.sub(r'[‘’]', "'", json_content)
            # 移除JSON字符串前后的空格
            json_content = json_content.strip()

            try:
                result = json.loads(json_content)
            except json.JSONDecodeError as e:
                print(f"[DEBUG] JSON解析失败，尝试修复: {e}")
                # 尝试修复：处理字段值中未转义的换行符和双引号
                
                # 1. 临时替换换行符，防止正则匹配不到多行内容
                # 注意：这里我们主要处理 string value 内部的换行
                
                # 更复杂的修复逻辑：
                # 我们假设结构是大体正确的，主要问题是 "content": "..." 内部的内容包含 " 或 \n
                
                def fix_json_value(match):
                    key = match.group(1)
                    val = match.group(2)
                    
                    # 1. 转义内部的双引号 (排除已经是转义的 \")
                    # 先把 \" 保护起来
                    val = val.replace('\\"', '《TEMP_QUOTE》')
                    # 把剩余的 " 变成 \"
                    val = val.replace('"', '\\"')
                    # 还原 \"
                    val = val.replace('《TEMP_QUOTE》', '\\"')
                    
                    # 2. 转义换行符
                    val = val.replace('\n', '\\n').replace('\r', '')
                    
                    return f'"{key}": "{val}"'

                # 匹配 "key": "value" 模式，value 可以包含换行，但非贪婪匹配可能在内部 " 处停止
                # 这种正则很难完美，针对特定字段进行修复可能更稳妥
                # 这里针对 "content" 和 "tips" 这种长文本字段做特殊处理
                
                fixed_content = json_content
                
                # 针对 content 字段修复: "content": "..."
                # 试图匹配 "content":\s*"  到  "(?:\s*[,}]) 之间的内容
                # 这是一个简化的启发式修复
                
                # 方案 B：使用更通用的字符替换
                # 如果是 expecting ',' delimiter，通常意味着在字符串内部遇到了双引号
                
                # 尝试先转义换行符
                fixed_content = re.sub(r'(?<=: ")(.*?)(?=")', lambda m: m.group(1).replace('\n', '\\n'), fixed_content, flags=re.DOTALL)
                
                try:
                    result = json.loads(fixed_content)
                except:
                   # 最后的兜底：如果还是失败，尝试用 dirty-json 或者手动提取
                   # 这里简化处理，如果实在解不开，返回默认值前再尝试一次暴力清理
                   fixed_content_2 = json_content.replace('\n', '\\n')
                   try:
                       result = json.loads(fixed_content_2)
                   except:
                       raise e

        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print(f"完整的JSON内容: {json_content}")
            # 使用默认分析结果作为备选
            result = {
                "sections": [
                    {
                        "title": "职业背景分析",
                        "content": "根据您提供的信息，您具有良好的职业背景和相关经验，适合目标岗位的要求。",
                        "tips": [
                            "在面试中突出您的核心技能和项目经验",
                            "使用具体数据和案例来支撑您的能力",
                            "重点展示与目标岗位相关的工作经历"
                        ]
                    },
                    {
                        "title": "面试策略建议",
                        "content": "基于您的背景和目标岗位，建议您采用以下面试策略。",
                        "tips": [
                            "提前了解目标公司的业务和文化",
                            "准备3-5个典型的项目案例，使用STAR法则进行描述",
                            "针对常见问题提前准备回答框架"
                        ]
                    }
                ]
            }
        except Exception as e:
            print(f"处理API结果时出错: {e}")
            # 使用默认分析结果作为备选
            result = {
                "sections": [
                    {
                        "title": "职业背景分析",
                        "content": "根据您提供的信息，您具有良好的职业背景和相关经验，适合目标岗位的要求。",
                        "tips": [
                            "在面试中突出您的核心技能和项目经验",
                            "使用具体数据和案例来支撑您的能力",
                            "重点展示与目标岗位相关的工作经历"
                        ]
                    },
                    {
                        "title": "面试策略建议",
                        "content": "基于您的背景和目标岗位，建议您采用以下面试策略。",
                        "tips": [
                            "提前了解目标公司的业务和文化",
                            "准备3-5个典型的项目案例，使用STAR法则进行描述",
                            "针对常见问题提前准备回答框架"
                        ]
                    }
                ]
            }
        
        # 保存到数据库
        try:
            # 删除用户旧的策略分析记录，只保留最新的一条
            try:
                InterviewStrategy.query.filter_by(user_id=user_id, type='analysis').delete()
            except Exception as e:
                print(f"删除旧策略分析记录失败: {e}")
            
            # 创建InterviewStrategy记录
            strategy = InterviewStrategy(
                user_id=user_id,
                resume_id=resume_id,
                type='analysis',
                background_info=background_info,
                directions=json.dumps(directions),
                result=json.dumps(result)
            )
            db.session.add(strategy)
            db.session.commit()
        except Exception as db_error:
            print(f"保存面试策略分析到数据库失败: {db_error}")
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"生成画像分析失败: {e}")
        # 使用默认分析结果作为备选
        result = {
            "sections": [
                {
                    "title": "职业背景分析",
                    "content": "根据您提供的信息，您具有良好的职业背景和相关经验，适合目标岗位的要求。",
                    "tips": [
                        "在面试中突出您的核心技能和项目经验",
                        "使用具体数据和案例来支撑您的能力",
                        "重点展示与目标岗位相关的工作经历"
                    ]
                },
                {
                    "title": "面试策略建议",
                    "content": "基于您的背景和目标岗位，建议您采用以下面试策略。",
                    "tips": [
                        "提前了解目标公司的业务和文化",
                        "准备3-5个典型的项目案例，使用STAR法则进行描述",
                        "针对常见问题提前准备回答框架"
                    ]
                }
            ],
            "message": get_message('analysis_gen_failed', locale, error=str(e))
        }
        
        return jsonify(result), 200

@bp.route('/analysis/history', methods=['GET'])
@auth_required
def get_analysis_history():
    """获取用户的策略分析历史记录API"""
    user_id = request.user_id
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/strategy/analysis/history - Request received: userId={user_id}")
    
    if not user_id:
        return jsonify({"error": get_message('missing_params', locale)}), 400
    
    try:
        # 获取用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": get_message('user_not_found', locale)}), 404
        
        # 获取用户的所有策略分析记录
        strategies = InterviewStrategy.query.filter_by(user_id=user_id, type='analysis').order_by(InterviewStrategy.created_at.desc()).all()
        
        # 转换为前端需要的格式
        history = []
        for strategy in strategies:
            history.append({
                "id": strategy.id,
                "resume_id": strategy.resume_id,
                "background_info": strategy.background_info,
                "directions": json.loads(strategy.directions) if strategy.directions else [],
                "created_at": strategy.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "result": json.loads(strategy.result) if strategy.result else {}
            })
        
        return jsonify(history), 200
    except Exception as e:
        print(f"获取策略分析历史失败: {e}")
        return jsonify({"error": get_message('get_analysis_history_failed', locale)}), 500

@bp.route('/questions', methods=['POST'])
@auth_required
def questions():
    """生成反问环节问题API"""
    data = request.get_json()
    company_name = data.get('companyName', '')
    position = data.get('position', '')
    question_types = data.get('questionTypes', [])
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
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
    print(f"[API LOG] /api/strategy/questions - Request received: companyName={company_name}, position={position}, questionTypes={question_types}, resumeId={resume_id}, userId={user_id}")
    
    # 获取简历内容
    resume_content = get_resume_content(resume_id, 'optimized')
    
    # 构建用户Prompt
    user_prompt = get_user_prompt(
        'strategy',
        locale,
        'questions_template',
        company=company_name,
        position=position,
        question_types=str(question_types),
        resume_content=resume_content
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": get_system_prompt('strategy', locale, 'questions_system')},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=8192
        )
        
        # 解析API返回结果
        api_result = response.choices[0].message.content
        
        try:
            # 清理可能的额外内容，只保留JSON部分
            start_idx = api_result.find('{')
            end_idx = api_result.rfind('}') + 1
            if start_idx == -1 or end_idx <= start_idx:
                raise ValueError("未找到有效的JSON结构")
            
            json_content = api_result[start_idx:end_idx]
            
            # 清理无效控制字符
            import re
            # 移除所有控制字符，除了制表符、换行符和回车符
            json_content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', json_content)
            
            # 清理JSON字符串中的中文引号
            json_content = re.sub(r'[“”]', '"', json_content)
            json_content = re.sub(r'[‘’]', "'", json_content)
            # 移除JSON字符串前后的空格
            json_content = json_content.strip()
            
            # 尝试解析JSON
            result = json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print(f"完整的JSON内容: {json_content}")
            # 使用默认问题作为备选
            result = {
                "questions": [
                    {
                        "content": "请问贵公司对这个岗位的核心考核指标是什么？",
                        "type": "岗位发展类",
                        "explanation": "了解岗位的考核指标，能够更好地理解公司对这个岗位的期望，也能判断自己是否适合这个岗位。"
                    },
                    {
                        "content": "请问这个团队目前的人员构成和分工是怎样的？",
                        "type": "团队文化类",
                        "explanation": "了解团队的人员构成和分工，能够更好地理解自己在团队中的定位和合作方式。"
                    },
                    {
                        "content": "请问贵公司的技术栈和未来的技术发展方向是什么？",
                        "type": "工作内容类",
                        "explanation": "了解公司的技术栈和发展方向，能够判断自己的技术能力是否匹配，也能了解未来的学习和发展机会。"
                    },
                    {
                        "content": "请问贵公司对新员工的培训和晋升机制是怎样的？",
                        "type": "岗位发展类",
                        "explanation": "了解公司的培训和晋升机制，能够判断自己在公司的成长空间和发展路径。"
                    },
                    {
                        "content": "请问贵公司的企业文化和价值观是什么？",
                        "type": "团队文化类",
                        "explanation": "了解公司的企业文化和价值观，能够判断自己是否认同公司的理念，是否能融入公司的文化氛围。"
                    }
                ]
            }
        except Exception as e:
            print(f"处理API结果时出错: {e}")
            # 使用默认问题作为备选
            result = {
                "questions": [
                    {
                        "content": "请问贵公司对这个岗位的核心考核指标是什么？",
                        "type": "岗位发展类",
                        "explanation": "了解岗位的考核指标，能够更好地理解公司对这个岗位的期望，也能判断自己是否适合这个岗位。"
                    },
                    {
                        "content": "请问这个团队目前的人员构成和分工是怎样的？",
                        "type": "团队文化类",
                        "explanation": "了解团队的人员构成和分工，能够更好地理解自己在团队中的定位和合作方式。"
                    },
                    {
                        "content": "请问贵公司的技术栈和未来的技术发展方向是什么？",
                        "type": "工作内容类",
                        "explanation": "了解公司的技术栈和发展方向，能够判断自己的技术能力是否匹配，也能了解未来的学习和发展机会。"
                    },
                    {
                        "content": "请问贵公司对新员工的培训和晋升机制是怎样的？",
                        "type": "岗位发展类",
                        "explanation": "了解公司的培训和晋升机制，能够判断自己在公司的成长空间和发展路径。"
                    },
                    {
                        "content": "请问贵公司的企业文化和价值观是什么？",
                        "type": "团队文化类",
                        "explanation": "了解公司的企业文化和价值观，能够判断自己是否认同公司的理念，是否能融入公司的文化氛围。"
                    }
                ]
            }
        
        # 保存到数据库
        try:
            # 删除用户旧的反问问题记录，只保留最新的一条
            try:
                InterviewStrategy.query.filter_by(user_id=user_id, type='questions').delete()
            except Exception as e:
                print(f"删除旧反问问题记录失败: {e}")
          
            # 创建InterviewStrategy记录
            strategy = InterviewStrategy(
                user_id=user_id,
                resume_id=resume_id,
                type='questions',
                company_name=company_name,
                position=position,
                question_types=json.dumps(question_types),
                result=json.dumps(result)
            )
            db.session.add(strategy)
            db.session.commit()
        except Exception as db_error:
            print(f"保存反问问题到数据库失败: {db_error}")
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"生成反问问题失败: {e}")
        # 使用默认问题作为备选
        result = {
            "questions": [
                {
                    "content": "请问贵公司对这个岗位的核心考核指标是什么？",
                    "type": "岗位发展类",
                    "explanation": "了解岗位的考核指标，能够更好地理解公司对这个岗位的期望，也能判断自己是否适合这个岗位。"
                },
                {
                    "content": "请问这个团队目前的人员构成和分工是怎样的？",
                    "type": "团队文化类",
                    "explanation": "了解团队的人员构成和分工，能够更好地理解自己在团队中的定位和合作方式。"
                },
                {
                    "content": "请问贵公司的技术栈和未来的技术发展方向是什么？",
                    "type": "工作内容类",
                    "explanation": "了解公司的技术栈和发展方向，能够判断自己的技术能力是否匹配，也能了解未来的学习和发展机会。"
                },
                {
                    "content": "请问贵公司对新员工的培训和晋升机制是怎样的？",
                    "type": "岗位发展类",
                    "explanation": "了解公司的培训和晋升机制，能够判断自己在公司的成长空间和发展路径。"
                },
                {
                    "content": "请问贵公司的企业文化和价值观是什么？",
                    "type": "团队文化类",
                    "explanation": "了解公司的企业文化和价值观，能够判断自己是否认同公司的理念，是否能融入公司的文化氛围。"
                }
            ]
        }
        
        return jsonify(result), 200

@bp.route('/questions/history', methods=['GET'])
@auth_required
def get_questions_history():
    """获取用户的反问问题历史记录API"""
    # 从request对象中获取用户ID，这是auth_required装饰器设置的
    user_id = request.user_id
    locale = request.headers.get('X-Locale', 'zh')
    
    # 打印请求参数
    print(f"[API LOG] /api/strategy/questions/history - Request received: userId={user_id}")
    
    if not user_id:
        return jsonify({"error": get_message('missing_params', locale)}), 400
    
    try:
        # 获取用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": get_message('user_not_found', locale)}), 404
        
        # 获取用户的所有反问问题记录
        strategies = InterviewStrategy.query.filter_by(user_id=user_id, type='questions').order_by(InterviewStrategy.created_at.desc()).all()
        
        # 转换为前端需要的格式
        history = []
        for strategy in strategies:
            history.append({
                "id": strategy.id,
                "resume_id": strategy.resume_id,
                "company_name": strategy.company_name,
                "position": strategy.position,
                "question_types": json.loads(strategy.question_types) if strategy.question_types else [],
                "created_at": strategy.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "result": json.loads(strategy.result) if strategy.result else {}
            })
        
        return jsonify(history), 200
    except Exception as e:
        print(f"获取反问问题历史失败: {e}")
        return jsonify({"error": get_message('get_questions_history_failed', locale)}), 500
