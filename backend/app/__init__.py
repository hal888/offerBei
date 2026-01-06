from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
import os

# 创建Flask应用实例
app = Flask(__name__)

# 配置CORS
CORS(app, origins=["https://interview.ailongdev.com", "http://localhost:5173"])
# 设置项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))

# 导入配置
from config import (
    DEEPSEEK_CONFIG, 
    SQLALCHEMY_DATABASE_URI, 
    SQLALCHEMY_TRACK_MODIFICATIONS, 
    SQLALCHEMY_POOL_SIZE, 
    SQLALCHEMY_MAX_OVERFLOW,
    MAIL_CONFIG,
    JWT_CONFIG,
    ALIYUN_ASR_CONFIG,
    ALIYUN_ASR_URL
)

# 配置SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_POOL_SIZE'] = SQLALCHEMY_POOL_SIZE
app.config['SQLALCHEMY_MAX_OVERFLOW'] = SQLALCHEMY_MAX_OVERFLOW

# 配置Flask-Mail
app.config['MAIL_SERVER'] = MAIL_CONFIG['server']
app.config['MAIL_PORT'] = MAIL_CONFIG['port']
app.config['MAIL_USERNAME'] = MAIL_CONFIG['username']
app.config['MAIL_PASSWORD'] = MAIL_CONFIG['password']
app.config['MAIL_USE_TLS'] = MAIL_CONFIG['use_tls']
app.config['MAIL_USE_SSL'] = MAIL_CONFIG['use_ssl']
app.config['MAIL_DEFAULT_SENDER'] = MAIL_CONFIG['default_sender']

# 初始化Flask-Mail
mail = Mail(app)

# 导入并初始化数据库
from .models import db

# 初始化SQLAlchemy
db.init_app(app)


# 导入路由
from .routes import resume, self_intro, question_bank, mock_interview, strategy, auth

# 注册蓝图
app.register_blueprint(resume)
app.register_blueprint(self_intro)
app.register_blueprint(question_bank)
app.register_blueprint(mock_interview)
app.register_blueprint(strategy)
app.register_blueprint(auth)

# 初始化数据库
with app.app_context():
    db.create_all()

# 添加调试路由，用于列出所有注册的路由
@app.route('/api/routes', methods=['GET'])
def list_routes():
    """列出所有注册的路由"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': rule.rule
        })
    return jsonify({'routes': routes}), 200