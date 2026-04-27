""" E-Commerce Models
    build using SQLAlchemy ORM
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime ,func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    products = relationship('Product', back_populates='category')
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=True)
    
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship('Category', back_populates='products')
    order_items = relationship('OrderItem', back_populates='product')




class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)

    orders = relationship('Order', back_populates='customer')


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    status = Column(String(20), default="pending")  # pending, paid, shipped
    total_price = Column(Float, default=0)
    created_at = Column(DateTime, default=func.now())
    order_date = Column(DateTime, default=func.now())
    shipping_address = Column(String(255), nullable=True)

    total_mount = Column(Float, default=0)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order" , cascade="all, delete-orphan" ,lazy=True)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price = Column(Float, default=0)

    order = relationship("Order", back_populates="items")
    product = relationship("Product" ,back_populates="order_items")