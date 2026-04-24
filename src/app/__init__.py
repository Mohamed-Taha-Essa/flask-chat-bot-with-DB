"""
Flask Application Factory

This module implements the Application Factory pattern, which is the recommended
approach for organizing larger Flask applications. It provides:

- Separation of concerns: App creation logic is isolated from the main entry point
- Testability: Easy to create test instances of the app with different configs
- Flexibility: Can create multiple app instances with different configurations
- Scalability: Extensions are properly initialized in one place
"""

import os
from flask import Flask
from flask_socketio import SocketIO

from app.core.config import settings
from app.core.auth import login_manager
from app.routes.auth import auth_bp
from app.routes.main import main_bp


socketio = SocketIO()


def create_app() -> Flask:
    """
    Application factory function that creates and configures the Flask app.
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Get the absolute path to templates folder
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    
    # Create Flask app instance
    app = Flask(__name__, template_folder=template_dir)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-key')
    
    # Initialize extensions
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Register error handlers and CLI commands here if needed
    
    return app