from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Product, Order
from app.redis_client import redis_client

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
@login_required
def check_admin():
    if not current_user.is_admin:
        flash('需要管理员权限')
        return redirect(url_for('main.index'))

@admin.route('/')
def dashboard():
    products = Product.query.all()
    orders = Order.query.all()
    return render_template('admin/dashboard.html', products=products, orders=orders)

@admin.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            stock=int(request.form.get('stock'))
        )
        db.session.add(product)
        db.session.commit()
        flash('商品添加成功')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_product.html')

@admin.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        db.session.commit()
        # 清除Redis缓存
        redis_client.delete_product(id)
        flash('商品更新成功')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_product.html', product=product)

@admin.route('/product/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    # 清除Redis缓存
    redis_client.delete_product(id)
    flash('商品删除成功')
    return redirect(url_for('admin.dashboard'))

@admin.route('/cache/clear')
def clear_cache():
    redis_client.clear_all_cache()
    flash('缓存已清理')
    return redirect(url_for('admin.dashboard'))
