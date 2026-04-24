"""
Flask Application Entry Point

This is the main entry point for the Flask application.
It uses the application factory pattern (defined in app/__init__.py) for
better code organization and testability.
"""

from app import create_app
from app.extensions import socketio
from app.core.config import settings
from flask import jsonify


app = create_app()


@app.route("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify(
        {
            "status": "ok",
            "message": "Service is running"
        }
    )


if __name__ == "__main__":
    socketio.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )