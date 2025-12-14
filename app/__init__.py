from flask import Flask
from flask_login import LoginManager
from app.models import db, User
from app.redis_client import redis_client
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    redis_client.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.admin import admin
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    
    with app.app_context():
        db.create_all()
        try:
            if redis_client.client:
                redis_client.client.ping()
                print('✓ Redis连接成功')
        except:
            redis_client.client = None
            print('✗ Redis未启动，缓存功能不可用')
    
    return app
