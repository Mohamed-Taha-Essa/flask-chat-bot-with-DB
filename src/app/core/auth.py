"""
Flask-Login Authentication Configuration

This module configures Flask-Login for user authentication and session management.

WHAT THIS FILE DOES:
- Initializes Flask-Login's LoginManager
- Provides the user_loader callback function required by Flask-Login
- Enables session-based authentication throughout the Flask application

WHY WE USE load_user:
Flask-Login requires a user_loader callback to reconstruct User objects from stored
session data. When a user makes a request with a valid session, Flask-Login calls
this function with the user_id stored in the session cookie to load the full User
object from the database. This allows Flask-Login to provide the current_user proxy
object in templates and views.

WHAT HAPPENS IF WE DON'T USE load_user:
- Flask-Login cannot load user objects from sessions
- current_user will always be None (AnonymousUserMixin)
- User authentication will fail on every request
- Session-based features like @login_required will not work
- Users will be logged out immediately after any page refresh
- The application will lose all user session management capabilities

The load_user function:
- Takes a user_id (string) from the session
- Queries the database to find the User with that ID
- Returns the User object if found, None if not found
- Uses a new database session for each call (stateless)
"""

from flask_login import LoginManager
from app.models import User
from app.db.database import SessionLocal  # Use SessionLocal for read-only operations


login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect unauthenticated users to login page
login_manager.login_message = 'Please log in to access this page.'  # Optional: custom message


@login_manager.user_loader
def load_user(user_id):
    """
    Load user from database by user_id.
    Uses SessionLocal directly (not context manager) because this is a read-only 
    operation and we need the returned user object to remain usable after the 
    session is closed. Flask-Login handles the session cleanup.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except Exception as e:
        return None
    finally:
        db.close()