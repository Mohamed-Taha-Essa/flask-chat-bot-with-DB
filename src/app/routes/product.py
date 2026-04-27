from flask import Blueprint, render_template, request, abort
from app.models.e_commerce import Product, Category
from app.db.database import get_db_session
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

product_bp = Blueprint('product', __name__)

@product_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    with get_db_session() as db:
        # Build query with filters
        products_query = db.query(Product).options(joinedload(Product.category))
        
        # Apply search filter
        if search:
            search_term = f'%{search}%'
            products_query = products_query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # Apply category filter
        if category_filter:
            products_query = products_query.join(Category).filter(
                Category.name.ilike(f'%{category_filter}%')
            )
        
        # Get total count for pagination
        total_products = products_query.count()
        
        # Get paginated products
        all_products = products_query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Calculate pagination info
        total_pages = (total_products + per_page - 1) // per_page
        has_prev = page > 1
        has_next = page < total_pages
        
        return render_template('e-commerce/producs_list.html',
            all_products=all_products,
            page=page,
            per_page=per_page,
            total_products=total_products,
            total_pages=total_pages,
            has_prev=has_prev,
            has_next=has_next,
            search=search,
            category_filter=category_filter
        )

@product_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    with get_db_session() as db:
        product = db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id).first()
        
        if not product:
            abort(404)
        
        return render_template('e-commerce/product_detail.html', product=product)