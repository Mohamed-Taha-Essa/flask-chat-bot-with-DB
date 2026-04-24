"""
Flask-Login Authentication Configuration

This module configures Flask-Login for user authentication and session management.

WHAT THIS FILE DOES:
- Registers the user_loader callback with Flask-Login (which is initialized in app.extensions)
- Provides the load_user function that reconstructs User objects from stored session data
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

from app.extensions import login_manager  # Import pre-initialized extension
from app.models import User
from app.db.database import SessionLocal  # Use SessionLocal for read-only operations


# Configure login_manager settings
login_manager.login_view = 'auth.login'  # Redirect to login page for protected routes
login_manager.login_message = 'Please log in to access this page.'


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