"""
Main routes for the Chat System application.
"""

from flask import Blueprint, render_template

# Create blueprint for main routes
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/index')
def index():
    """Display the home page."""
    return render_template('home/index.html')
