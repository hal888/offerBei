from flask_mail import Message
from .. import mail
from flask import render_template_string

class EmailUtil:
    @staticmethod
    def send_verification_code(email, code):
        """发送邮箱验证码"""
        subject = "Offer贝 - 邮箱验证码"
        html_body = f"""
        <h2>Offer贝邮箱验证码</h2>
        <p>您的邮箱验证码是：<strong>{code}</strong></p>
        <p>验证码将在15分钟后过期，请尽快使用。</p>
        <p>如果您没有请求此验证码，请忽略此邮件。</p>
        <p>---</p>
        <p>Offer贝团队</p>
        """
        
        message = Message(subject=subject, recipients=[email], html=html_body)
        mail.send(message)
    
    @staticmethod
    def send_reset_password_link(email, reset_link):
        """发送密码重置链接"""
        subject = "Offer贝 - 密码重置请求"
        html_body = f"""
        <h2>Offer贝密码重置</h2>
        <p>您请求重置您的Offer贝账号密码。请点击以下链接重置密码：</p>
        <p><a href="{reset_link}" target="_blank">点击重置密码</a></p>
        <p>或者复制以下链接到浏览器中打开：</p>
        <p>{reset_link}</p>
        <p>该链接将在24小时后过期，请尽快使用。</p>
        <p>如果您没有请求密码重置，请忽略此邮件。</p>
        <p>---</p>
        <p>Offer贝团队</p>
        """
        
        message = Message(subject=subject, recipients=[email], html=html_body)
        mail.send(message)