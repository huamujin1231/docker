import pymysql
from app import create_app
from app.models import db, User, Product
from werkzeug.security import generate_password_hash

print('重置MySQL数据库...')

# 连接MySQL并重置数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',  # 改成你的MySQL密码
    charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # 删除并重新创建数据库
        cursor.execute("DROP DATABASE IF EXISTS ecommerce")
        cursor.execute("CREATE DATABASE ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print('✓ 数据库重置完成')
finally:
    connection.close()

# 创建表和初始数据
app = create_app()

with app.app_context():
    print('创建表结构...')
    db.create_all()
    
    print('添加管理员账号...')
    admin = User(
        username='admin',
        email='admin@ecommerce.com',
        password=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    
    print('添加示例商品...')
    products = [
        Product(
            name='iPhone 15 Pro',
            description='Apple最新旗舰手机，搭载A17 Pro芯片',
            price=7999.00,
            stock=25
        ),
        Product(
            name='MacBook Pro 14英寸',
            description='M3芯片，专业级性能笔记本电脑',
            price=14999.00,
            stock=15
        ),
        Product(
            name='AirPods Pro 2代',
            description='主动降噪无线耳机，空间音频',
            price=1899.00,
            stock=50
        ),
        Product(
            name='iPad Air',
            description='轻薄便携平板电脑，M1芯片',
            price=4399.00,
            stock=30
        ),
        Product(
            name='Apple Watch Series 9',
            description='智能手表，健康监测专家',
            price=2999.00,
            stock=40
        )
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    
    print('✓ 数据库重置并初始化完成！')
    print('✓ 管理员账号: admin / admin123')
    print('✓ 已添加5个示例商品')
    print('✓ 可以在Navicat中查看整洁的数据结构')