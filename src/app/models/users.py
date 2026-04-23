"""

This module defines the User model for the application. 
It uses SQLAlchemy to create a table in the database that will store user information 
such as id, username, email, and password.

"""

from sqlalchemy import Column ,Integer,String ,DateTime ,func
from app.db.database import Base
from flask_login import UserMixin

from werkzeug.security import generate_password_hash ,check_password_hash

class User(Base ,UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=func.now())
    roles = Column(String(50), default='customer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_access_to_table(self, table_name):
        rol_permissions = {
            'admin': ['orders', 'products', 'users' , 'category'  , 'chat_sessions'],
            'manager': ['orders', 'products'],
            'customer': ['orders', 'products']
        }

        return table_name in rol_permissions.get(self.roles, [])