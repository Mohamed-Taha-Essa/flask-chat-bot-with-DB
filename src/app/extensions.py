"""
Flask Extensions Initialization

This module centralizes the initialization of all Flask extensions.
Extensions are created here WITHOUT being bound to an app instance.

This approach:
- Avoids circular imports completely
- Makes extensions available to all modules (routes, models, etc.)
- Follows Flask best practices for larger applications
- Makes testing easier (can use different app instances with same extensions)

Extensions are initialized with an app instance in the factory (app/__init__.py)
"""

from flask_login import LoginManager
from flask_socketio import SocketIO

# Create extension instances (not yet bound to any Flask app)
login_manager = LoginManager()
socketio = SocketIO()
