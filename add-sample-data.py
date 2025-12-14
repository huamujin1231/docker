#!/usr/bin/env python3
"""添加示例数据到数据库"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

def add_sample_data():
    """添加示例数据"""
    app = create_app()
    with app.app_context():
        try:
            # 创建分类表
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # 创建商品表
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    price DECIMAL(10,2) NOT NULL,
                    stock INT DEFAULT 0,
                    category_id INT,
                    image_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """))
            
            # 创建用户表
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # 插入分类数据
            categories = [
                ('电子产品', '手机、电脑、数码设备'),
                ('服装鞋帽', '男装、女装、童装、鞋子'),
                ('家居用品', '家具、装饰、生活用品'),
                ('图书音像', '图书、音乐、电影'),
                ('运动户外', '运动器材、户外用品')
            ]
            
            for name, desc in categories:
                db.session.execute(text(
                    "INSERT IGNORE INTO categories (name, description) VALUES (:name, :desc)"
                ), {"name": name, "desc": desc})
            
            # 插入商品数据
            products = [
                ('iPhone 15 Pro', '最新款苹果手机，性能强劲', 8999.00, 50, 1, 'https://via.placeholder.com/300x300?text=iPhone+15+Pro'),
                ('MacBook Air M3', '轻薄便携笔记本电脑', 9999.00, 30, 1, 'https://via.placeholder.com/300x300?text=MacBook+Air'),
                ('AirPods Pro', '主动降噪无线耳机', 1999.00, 100, 1, 'https://via.placeholder.com/300x300?text=AirPods+Pro'),
                ('Nike运动鞋', '舒适透气运动鞋', 599.00, 80, 2, 'https://via.placeholder.com/300x300?text=Nike+Shoes'),
                ('Adidas卫衣', '时尚休闲卫衣', 399.00, 60, 2, 'https://via.placeholder.com/300x300?text=Adidas+Hoodie'),
                ('宜家书桌', '简约现代办公桌', 899.00, 25, 3, 'https://via.placeholder.com/300x300?text=IKEA+Desk'),
                ('小米台灯', 'LED护眼台灯', 199.00, 120, 3, 'https://via.placeholder.com/300x300?text=Xiaomi+Lamp'),
                ('Python编程书', 'Python从入门到精通', 89.00, 200, 4, 'https://via.placeholder.com/300x300?text=Python+Book'),
                ('瑜伽垫', '防滑环保瑜伽垫', 129.00, 150, 5, 'https://via.placeholder.com/300x300?text=Yoga+Mat'),
                ('哑铃套装', '可调节重量哑铃', 299.00, 40, 5, 'https://via.placeholder.com/300x300?text=Dumbbells')
            ]
            
            for name, desc, price, stock, cat_id, img in products:
                db.session.execute(text("""
                    INSERT IGNORE INTO products (name, description, price, stock, category_id, image_url) 
                    VALUES (:name, :desc, :price, :stock, :cat_id, :img)
                """), {
                    "name": name, "desc": desc, "price": price, 
                    "stock": stock, "cat_id": cat_id, "img": img
                })
            
            # 创建管理员用户
            from werkzeug.security import generate_password_hash
            admin_password = generate_password_hash('admin123')
            
            db.session.execute(text("""
                INSERT IGNORE INTO users (username, email, password_hash, is_admin) 
                VALUES ('admin', 'admin@example.com', :password, TRUE)
            """), {"password": admin_password})
            
            db.session.commit()
            print("✅ 示例数据添加成功！")
            
            # 验证数据
            result = db.session.execute(text("SELECT COUNT(*) as count FROM products")).fetchone()
            print(f"📊 商品总数: {result.count}")
            
            result = db.session.execute(text("SELECT COUNT(*) as count FROM categories")).fetchone()
            print(f"📊 分类总数: {result.count}")
            
        except Exception as e:
            print(f"❌ 添加数据失败: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_sample_data()