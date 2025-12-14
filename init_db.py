from app import create_app
from app.models import db, User, Product
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    admin = User(username='admin', email='admin@example.com', 
                 password=generate_password_hash('admin123'), is_admin=True)
    db.session.add(admin)
    
    products = [
        Product(name='iPhone 15', description='最新款苹果手机', price=5999, stock=50),
        Product(name='MacBook Pro', description='专业笔记本电脑', price=12999, stock=30),
        Product(name='AirPods Pro', description='无线降噪耳机', price=1999, stock=100),
    ]
    
    for p in products:
        db.session.add(p)
    
    db.session.commit()
    print('数据库初始化完成！')
    print('管理员账号: admin / admin123')
