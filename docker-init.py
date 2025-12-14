#!/usr/bin/env python3
"""Docker环境数据库初始化脚本"""

import time
import sys
from app import create_app, db

def wait_for_db():
    """等待数据库连接"""
    app = create_app()
    with app.app_context():
        max_retries = 30
        for i in range(max_retries):
            try:
                with db.engine.connect() as conn:
                    conn.execute(db.text('SELECT 1'))
                print("数据库连接成功")
                return True
            except Exception as e:
                print(f"等待数据库连接... ({i+1}/{max_retries})")
                time.sleep(2)
        return False

def init_database():
    """初始化数据库"""
    app = create_app()
    with app.app_context():
        # 创建表
        db.create_all()
        print("数据库表创建完成")
        
        # 添加示例数据
        add_sample_data()
        
        # 提交事务
        db.session.commit()
        print("数据库初始化完成")

def add_sample_data():
    """添加示例数据"""
    from app.models import Product, User
    from werkzeug.security import generate_password_hash
    
    # 检查是否已有数据
    if Product.query.first():
        print("示例数据已存在，跳过")
        return
    
    # 添加示例商品
    products = [
        Product(name='iPhone 15 Pro', description='最新款苹果手机，性能强劲', price=8999.00, stock=50, image='iphone.jpg'),
        Product(name='MacBook Air M3', description='轻薄便携笔记本电脑', price=9999.00, stock=30, image='macbook.jpg'),
        Product(name='AirPods Pro', description='主动降噪无线耳机', price=1999.00, stock=100, image='airpods.jpg'),
        Product(name='Nike运动鞋', description='舒适透气运动鞋', price=599.00, stock=80, image='nike.jpg'),
        Product(name='Adidas卫衣', description='时尚休闲卫衣', price=399.00, stock=60, image='adidas.jpg'),
        Product(name='宜家书桌', description='简约现代办公桌', price=899.00, stock=25, image='desk.jpg'),
        Product(name='小米台灯', description='LED护眼台灯', price=199.00, stock=120, image='lamp.jpg'),
        Product(name='Python编程书', description='Python从入门到精通', price=89.00, stock=200, image='book.jpg'),
        Product(name='瑜伽垃', description='防滑环保瑜伽垃', price=129.00, stock=150, image='yoga.jpg'),
        Product(name='哑铃套装', description='可调节重量哑铃', price=299.00, stock=40, image='dumbbells.jpg')
    ]
    
    for product in products:
        db.session.add(product)
    
    # 添加管理员用户
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
    
    print(f"✅ 添加了 {len(products)} 个示例商品和管理员账户")

if __name__ == '__main__':
    if wait_for_db():
        init_database()
    else:
        print("数据库连接失败")
        sys.exit(1)