from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Product, Cart, Order, OrderItem
from app.redis_client import redis_client

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route('/product/<int:id>')
def product_detail(id):
    # 尝试从Redis获取缓存
    cached = redis_client.get_product(id)
    if cached:
        product = Product.query.get_or_404(id)
    else:
        product = Product.query.get_or_404(id)
        # 缓存商品信息
        redis_client.cache_product(id, {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock
        })
    return render_template('product.html', product=product)

@main.route('/cart')
@login_required
def cart():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in items)
    # 缓存购物车数量
    redis_client.cache_cart_count(current_user.id, len(items))
    return render_template('cart.html', items=items, total=total)

@main.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id)
        db.session.add(cart_item)
    db.session.commit()
    flash('已添加到购物车')
    return redirect(url_for('main.index'))

@main.route('/remove_from_cart/<int:id>')
@login_required
def remove_from_cart(id):
    cart_item = Cart.query.get_or_404(id)
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('main.cart'))

@main.route('/checkout', methods=['POST'])
@login_required
def checkout():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('购物车为空')
        return redirect(url_for('main.cart'))
    
    total = sum(item.product.price * item.quantity for item in items)
    order = Order(user_id=current_user.id, total=total)
    db.session.add(order)
    db.session.flush()
    
    for item in items:
        order_item = OrderItem(order_id=order.id, product_id=item.product_id, 
                              quantity=item.quantity, price=item.product.price)
        db.session.add(order_item)
        db.session.delete(item)
    
    db.session.commit()
    flash('订单创建成功')
    return redirect(url_for('main.orders'))

@main.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)
