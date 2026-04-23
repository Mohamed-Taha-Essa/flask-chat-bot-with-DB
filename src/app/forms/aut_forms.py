"""
Authentication Forms using Flask-WTF for server-side validation and CSRF protection.
Best practices:
- Email validation using built-in validators
- Password requirements enforcement
- CSRF token protection
- Form reusability across templates
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
    Regexp,
)
from app.models import User
from app.db.database import get_db_session


class LoginForm(FlaskForm):
    """Form for user login with email and password validation."""
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Invalid email address"),
        ],
        render_kw={"placeholder": "Enter your email"}
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
        ],
        render_kw={"placeholder": "Enter your password"}
    )
    
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    """Form for user registration with comprehensive validation."""
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=50, message="Username must be between 3 and 50 characters"),
            Regexp(
                '^[A-Za-z0-9_]+$',
                message="Username can only contain letters, numbers, and underscores"
            ),
        ],
        render_kw={"placeholder": "Enter username"}
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Invalid email address"),
        ],
        render_kw={"placeholder": "Enter your email"}
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
            Length(min=6, message="Password must be at least 6 characters long"),
        ],
        render_kw={"placeholder": "Enter password (min 6 characters)"}
    )
    
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo('password', message="Passwords must match"),
        ],
        render_kw={"placeholder": "Confirm password"}
    )
    
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        """Check if username already exists in database using context manager."""
        with get_db_session() as db:
            existing_user = db.query(User).filter(
                User.username == field.data
            ).first()
            if existing_user:
                raise ValidationError("Username already taken. Please choose another.")
    
    def validate_email(self, field):
        """Check if email already exists in database using context manager."""
        with get_db_session() as db:
            existing_user = db.query(User).filter(
                User.email == field.data
            ).first()
            if existing_user:
                raise ValidationError("Email already registered. Please use a different email.")
