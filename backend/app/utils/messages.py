MESSAGES = {
    'zh': {
        # Auth
        'email_required': '邮箱不能为空',
        'email_invalid': '邮箱格式无效：{error}',
        'verification_code_sent': '验证码已发送到您的邮箱',
        'send_code_failed': '发送验证码失败，请检查邮箱配置或稍后重试',
        'email_password_code_required': '邮箱、密码和验证码不能为空',
        'password_min_length': '密码长度不能少于8位',
        'email_registered': '该邮箱已被注册',
        'get_code_first': '请先获取验证码',
        'code_error': '验证码错误',
        'code_expired': '验证码已过期',
        'email_password_required': '邮箱和密码不能为空',
        'account_locked': '账号已被锁定，请{minutes}分钟后再试',
        'login_failure_limit': '登录失败次数过多，账号已被锁定',
        'login_failed': '邮箱或密码错误',
        'reset_link_sent': '如果该邮箱已注册，重置链接将发送到您的邮箱',
        'send_link_failed': '发送重置链接失败，请检查邮箱配置或稍后重试',
        'email_token_password_required': '邮箱、重置令牌和新密码不能为空',
        'user_not_found': '用户不存在',
        'invalid_token': '无效的重置令牌',
        'token_expired': '重置令牌已过期',
        'password_reset_success': '密码重置成功',
        'invalid_auth_header': '无效的认证头',
        'invalid_token_error': '无效或过期的令牌',
        'logout_success': '退出登录成功',
        'login_required': '请先登录',
        
        # Resume
        'file_required': '请选择文件',
        'file_empty': '文件为空',
        'file_type_error': '只支持PDF文件',
        'upload_success': '简历上传成功',
        'upload_failed': '简历上传失败：{error}',
        'analysis_success': '简历分析完成',
        'analysis_failed': '简历分析失败：{error}',
        
        # Mock Interview
        'resume_required': '请先上传简历',
        'interview_started': '面试已开始',
        'start_failed': '开始面试失败：{error}',
        'interview_ended': '面试已结束',
        'end_failed': '结束面试失败：{error}',
        'answer_required': '回答内容不能为空',
        'interview_not_found': '面试记录不存在',
        'answer_success': '回答已接收',
        'answer_failed': '处理回答失败：{error}',
        'audio_required': '请上传音频文件',
        'speech_unsupported': '您的浏览器不支持语音识别',
        'speech_failed': '语音识别失败：{error}',
        'speech_success': '语音识别成功',

        # Question Bank
        'question_bank_generated': '题库生成成功',
        'generate_failed': '生成题库失败：{error}',

        # Self Intro
        'intro_generated': '自我介绍生成成功',
        'intro_failed': '生成自我介绍失败：{error}',

        # Strategy
        'analysis_generated': '画像分析生成成功',
        'analysis_gen_failed': '生成画像分析失败：{error}',
        'questions_generated': '反问问题生成成功',
        'questions_gen_failed': '生成反问问题失败：{error}',
        'get_analysis_history_failed': '获取画像分析历史失败',
        'get_questions_history_failed': '获取反问问题历史失败',
        
        # Generic
        'missing_params': '缺少必要参数',
        'get_question_bank_failed': '获取题库失败',
        'get_intro_failed': '获取自我介绍失败',
    },
    'en': {
        # Auth
        'email_required': 'Email is required',
        'email_invalid': 'Invalid email format: {error}',
        'verification_code_sent': 'Verification code sent to your email',
        'send_code_failed': 'Failed to send verification code, please check email config or try again later',
        'email_password_code_required': 'Email, password and verification code are required',
        'password_min_length': 'Password must be at least 8 characters',
        'email_registered': 'Email already registered',
        'get_code_first': 'Please get verification code first',
        'code_error': 'Invalid verification code',
        'code_expired': 'Verification code expired',
        'email_password_required': 'Email and password are required',
        'account_locked': 'Account locked, please try again in {minutes} minutes',
        'login_failure_limit': 'Too many failed login attempts, account locked',
        'login_failed': 'Invalid email or password',
        'reset_link_sent': 'If the email is registered, a reset link will be sent to it',
        'send_link_failed': 'Failed to send reset link, please check email config or try again later',
        'email_token_password_required': 'Email, reset token and new password are required',
        'user_not_found': 'User not found',
        'invalid_token': 'Invalid reset token',
        'token_expired': 'Reset token expired',
        'password_reset_success': 'Password reset successfully',
        'invalid_auth_header': 'Invalid authorization header',
        'invalid_token_error': 'Invalid or expired token',
        'logout_success': 'Logged out successfully',
        'login_required': 'Please login first',

        # Resume
        'file_required': 'Please select a file',
        'file_empty': 'File is empty',
        'file_type_error': 'Only PDF files are supported',
        'upload_success': 'Resume uploaded successfully',
        'upload_failed': 'Failed to upload resume: {error}',
        'analysis_success': 'Resume analysis completed',
        'analysis_failed': 'Failed to analyze resume: {error}',

        # Mock Interview
        'resume_required': 'Please upload resume first',
        'interview_started': 'Interview started',
        'start_failed': 'Failed to start interview: {error}',
        'interview_ended': 'Interview ended',
        'end_failed': 'Failed to end interview: {error}',
        'answer_required': 'Answer cannot be empty',
        'interview_not_found': 'Interview record not found',
        'answer_success': 'Answer received',
        'answer_failed': 'Failed to process answer: {error}',
        'audio_required': 'Please upload audio file',
        'speech_unsupported': 'Your browser does not support speech recognition',
        'speech_failed': 'Speech recognition failed: {error}',
        'speech_success': 'Speech recognition successful',

        # Question Bank
        'question_bank_generated': 'Question bank generated successfully',
        'generate_failed': 'Failed to generate question bank: {error}',

        # Self Intro
        'intro_generated': 'Self-introduction generated successfully',
        'intro_failed': 'Failed to generate self-introduction: {error}',

        # Strategy
        'analysis_generated': 'Profile analysis generated successfully',
        'analysis_gen_failed': 'Failed to generate profile analysis: {error}',
        'questions_generated': 'Interview questions generated successfully',
        'questions_gen_failed': 'Failed to generate interview questions: {error}',
        'get_analysis_history_failed': 'Failed to get profile analysis history',
        'get_questions_history_failed': 'Failed to get interview questions history',
        
        # Generic
        'missing_params': 'Missing required parameters',
        'get_question_bank_failed': 'Failed to get question bank',
        'get_intro_failed': 'Failed to get self-introduction',
    }
}

def get_message(key, locale='zh', **kwargs):
    """
    获取指定语言的消息
    :param key: 消息键
    :param locale: 语言代码 ('zh' 或 'en')
    :param kwargs: 格式化参数
    :return: 翻译后的消息
    """
    # 默认使用中文
    if locale not in MESSAGES:
        locale = 'zh'
    
    # 获取消息字典
    lang_messages = MESSAGES.get(locale, MESSAGES['zh'])
    
    # 获取消息模板，如果key不存在则默认返回中文消息（如果中文也没有则返回key）
    message_template = lang_messages.get(key)
    if not message_template and locale != 'zh':
        message_template = MESSAGES['zh'].get(key, key)
    
    if not message_template:
        return key

    # 尝试格式化消息
    try:
        if kwargs:
            return message_template.format(**kwargs)
        return message_template
    except Exception:
        return message_template
