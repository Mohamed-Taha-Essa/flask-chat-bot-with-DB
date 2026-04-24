"""
Authentication related routes and functions for login, logout, and register.
Best practices:
- Uses Flask-Login for session management
- Database context manager for safe session handling
- Form validation with Flask-WTF
- Proper error handling and flash messages
- Secure password hashing with werkzeug
"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app.models import User
from app.db.database import get_db_session
from app.forms.aut_forms import LoginForm, RegisterForm

# Create blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    GET: Display registration form
    POST: Process registration form submission
    """
    # Redirect if user already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        try:
            # Use context manager for database session
            with get_db_session() as db:
                # Create new user instance
                new_user = User(
                    username=form.username.data,
                    email=form.email.data,
                    roles='customer'  # Default role for new users
                )
                
                # Set password using the model's method (hashes the password)
                new_user.set_password(form.password.data)
                
                # Add and commit user to database
                db.add(new_user)
                db.flush()  # Get the user ID before commit
                
                flash(
                    f'Account created successfully! Welcome {form.username.data}. Please log in.',
                    'success'
                )
                return redirect(url_for('auth.login'))
        
        except Exception as e:
            flash(f'An error occurred during registration: {str(e)}', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    GET: Display login form
    POST: Process login form submission
    """
    # Redirect if user already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            # Use context manager for database session
            with get_db_session() as db:
                # Find user by email
                user = db.query(User).filter(
                    User.email == form.email.data
                ).first()
                
                # Check if user exists and password is correct
                if user is None or not user.check_password(form.password.data):
                    flash('Invalid email or password. Please try again.', 'error')
                    return redirect(url_for('auth.login'))
                
                # Log the user in and create session
                login_user(user, remember=True)
                
                # Get next page from request args or redirect to index
                next_page = request.args.get('next')
                
                flash(f'Welcome back, {user.username}!', 'success')
                
                # Validate next_page to prevent open redirect
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('main.index'))
        
        except Exception as e:
            flash(f'An error occurred during login: {str(e)}', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    Requires user to be authenticated.
    """
    username = current_user.username
    logout_user()
    flash(f'You have been logged out. Goodbye, {username}!', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """
    Display user profile information.
    Requires user to be authenticated.
    """
    try:
        with get_db_session() as db:
            user = db.query(User).filter(User.id == current_user.id).first()
            
            if not user:
                flash('User not found.', 'error')
                return redirect(url_for('main.index'))
            
            return render_template('auth/profile.html', user=user)
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('main.index'))


