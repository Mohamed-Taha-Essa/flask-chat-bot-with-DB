import os
from flask import Flask , jsonify
from flask_migrate import Migrate
from app.core.config import settings

from flask_socketio import SocketIO
from app.core.auth import login_manager
from app.db.database import engine

from app.views.auth import auth_bp
from app.views.main import main_bp


socketio = SocketIO()   
 
# gobla migrate object 
migrate = Migrate()
def creat_app()->Flask :
    # Get the absolute path to templates folder
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app/templates'))
    
    app = Flask(__name__, template_folder=template_dir)
    login_manager.init_app(app)
    socketio.init_app(app , cors_allowed_origins="*")

    app.config['SECRET_KEY'] = 'super-secret-key'

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    migrate.init_app(app , db= engine, directory='migrations')

    return app 



app = creat_app()


@app.route("/health")
def health_check():
    return jsonify(
        {
            "status": "ok",
            "message": "Task service is running"
        }
    )

if __name__ == "__main__":
    socketio.run(
        app,
        host = settings.HOST,
        port = settings.PORT,
        debug = settings.DEBUG 
    )