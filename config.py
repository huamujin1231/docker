import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MySQL配置 - 支持环境变量
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123456@localhost:3306/ecommerce?charset=utf8mb4'
    
    # Redis配置 - 支持环境变量
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://127.0.0.1:6379/0'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0
