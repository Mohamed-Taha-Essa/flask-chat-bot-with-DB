"""
this file for admin dashboard in flask 
"""

from app.models.chat import ChatSession 
from app.models.e_commerce import Category ,Product ,Customer ,Order ,OrderItem
from app.models.users import User 
from app.db.database import get_db_session
from flask import Blueprint ,render_template ,request ,flash ,redirect ,url_for
from flask_login import login_required ,current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import func
from sqlalchemy.orm import joinedload

admin_bp = Blueprint('admin' , __name__, template_folder='templates' )

@admin_bp.route('/admin')
@login_required
def admin():
    with get_db_session() as db:
        all_users = db.query(User).all()
        all_chat_sessions = db.query(ChatSession).options(joinedload(ChatSession.user)).all()
        all_categories = db.query(Category).all()
        all_products = db.query(Product).options(joinedload(Product.category)).all()
        all_customers = db.query(Customer).all()
        all_orders = db.query(Order).options(joinedload(Order.customer)).all()
        all_order_items = db.query(OrderItem).options(joinedload(OrderItem.product)).all()

        return render_template('admin/admin.html' ,
         username=current_user.username,
         all_users=all_users,
         all_chat_sessions=all_chat_sessions,
         all_categories=all_categories,
         all_products=all_products,
         all_customers=all_customers,
         all_orders=all_orders,
         all_order_items=all_order_items
         )

@admin_bp.route('/admin/users')
@login_required
def users():
    with get_db_session() as db:
        all_users = db.query(User).all()
        return render_template('admin/users.html',
         username=current_user.username,
         all_users=all_users
         )

@admin_bp.route('/admin/products')
@login_required
def products():
    with get_db_session() as db:
        all_products = db.query(Product).options(joinedload(Product.category)).all()
        return render_template('admin/products.html',
         username=current_user.username,
         all_products=all_products
         )

@admin_bp.route('/admin/categories')
@login_required
def categories():
    with get_db_session() as db:
        all_categories = db.query(Category).all()
        return render_template('admin/categories.html',
         username=current_user.username,
         all_categories=all_categories
         )

@admin_bp.route('/admin/orders')
@login_required
def orders():
    with get_db_session() as db:
        all_orders = db.query(Order).options(joinedload(Order.customer)).all()
        return render_template('admin/orders.html',
         username=current_user.username,
         all_orders=all_orders
         )

@admin_bp.route('/admin/customers')
@login_required
def customers():
    with get_db_session() as db:
        all_customers = db.query(Customer).all()
        return render_template('admin/customers.html',
         username=current_user.username,
         all_customers=all_customers
         )

@admin_bp.route('/admin/chat-sessions')
@login_required
def chat_sessions():
    with get_db_session() as db:
        all_chat_sessions = db.query(ChatSession).options(joinedload(ChatSession.user)).all()
        return render_template('admin/chat_sessions.html',
         username=current_user.username,
         all_chat_sessions=all_chat_sessions
         )

@admin_bp.route('/admin/order-items')
@login_required
def order_items():
    with get_db_session() as db:
        all_order_items = db.query(OrderItem).options(joinedload(OrderItem.product)).all()
        return render_template('admin/order_items.html',
         username=current_user.username,
         all_order_items=all_order_items
         )
