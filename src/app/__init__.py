"""
Flask Application Factory

This module implements the Application Factory pattern, which is the recommended
approach for organizing larger Flask applications. It provides:

- Separation of concerns: App creation logic is isolated from the main entry point
- Testability: Easy to create test instances of the app with different configs
- Flexibility: Can create multiple app instances with different configurations
- Scalability: Extensions are properly initialized in one place

Extensions are defined in extensions.py and initialized here with the app instance.
"""

import os
from flask import Flask

from app.core.config import settings
from app.extensions import login_manager, socketio  # Import pre-created extension instances

# Import auth to register load_user callback with login_manager
import app.core.auth  # noqa: F401

# Routes can safely import extensions from app.extensions
from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.chat import chat_bp


def create_app() -> Flask:
    """
    Application factory function that creates and configures the Flask app.
    
    This function:
    - Creates a Flask app instance
    - Configures it with settings
    - Initializes extensions with the app
    - Registers blueprints
    
    Returns:
        Flask: Configured Flask application instance
    """
   
    
    # Get the absolute path to templates folder
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    
    # Create Flask app instance
    app = Flask(__name__, template_folder=template_dir)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-key')
    
    # Initialize extensions with the app instance
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    
    return app