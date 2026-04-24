"""
FLASK PROJECT ARCHITECTURE - BEST PRACTICES IMPLEMENTED
=======================================================

This document explains the professional Flask project structure implemented
to solve circular import issues and follow Flask community best practices.

PROBLEM SOLVED:
- Previous structure had circular imports between app/__init__.py and routes
- Extensions (socketio, login_manager) were creating circular dependencies
- Routes couldn't import extensions without breaking the app initialization

SOLUTION: Separation of Concerns with extensions.py
====================================================

File Structure:
├── app/
│   ├── __init__.py          ← Application Factory (creates Flask app)
│   ├── extensions.py        ← Extension initialization (NEW - KEY FILE)
│   ├── core/
│   │   ├── auth.py          ← Auth logic + callbacks
│   │   └── config.py        ← Configuration
│   ├── routes/              ← Blueprint routes
│   ├── models/              ← SQLAlchemy models
│   ├── db/                  ← Database setup
│   └── templates/           ← HTML templates
└── main.py                  ← Entry point

KEY PRINCIPLES:

1. EXTENSIONS (app/extensions.py)
   - Centralizes extension initialization
   - Extensions created WITHOUT Flask app binding
   - Imported by routes, auth, and factory
   - Completely avoids circular imports
   
2. FACTORY (app/__init__.py)
   - Creates Flask app instance
   - Binds extensions to the app
   - Registers blueprints
   - Imports auth to register callbacks

3. AUTH (app/core/auth.py)
   - Imports login_manager from app.extensions
   - Registers callbacks (@login_manager.user_loader)
   - Pure logic, no app creation

4. ROUTES (app/routes/*.py)
   - Import extensions from app.extensions
   - Register with app via blueprints
   - No circular imports possible

5. ENTRY POINT (main.py)
   - Imports create_app from app
   - Imports socketio from app.extensions
   - Clean and simple

IMPORT ORDER (avoids circular imports):

1. main.py imports create_app
   ↓
2. app/__init__.py imports extensions
   ↓
3. app/__init__.py imports auth
   ↓
4. auth.py imports login_manager from extensions
   ↓
5. create_app() imports routes
   ↓
6. routes import extensions (already loaded)
   ↓
✓ No circular dependencies!

WHY THIS IS BEST PRACTICE:

✅ Completely eliminates circular imports
✅ Easy to test (can create test app instances)
✅ Follows Flask community patterns
✅ Scalable (easy to add new extensions)
✅ Clear separation of concerns
✅ Professional production-ready structure
✅ Extensions are centralized and documented
✅ No import side effects

USAGE EXAMPLES:

# In routes (app/routes/your_route.py):
from app.extensions import socketio, login_manager

# In auth callbacks (app/core/auth.py):
from app.extensions import login_manager

# In main entry point (main.py):
from app import create_app
from app.extensions import socketio

# In tests:
from app import create_app
app = create_app()  # Fresh app instance for each test

REFERENCES:
- Flask Official: https://flask.palletsprojects.com/patterns/appfactories/
- Application Factories: https://flask.palletsprojects.com/patterns/appfactories/
- Flask Extensions: https://flask.palletsprojects.com/docs/latest/extensions/
"""
