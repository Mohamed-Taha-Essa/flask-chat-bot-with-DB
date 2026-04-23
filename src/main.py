from flask import Flask , jsonify
from flask_migrate import Migrate
from app.core.config import settings

from flask_socketio import SocketIO
from app.core.auth import login_manager
from app.db.database import engine
socketio = SocketIO()   
 
# gobla migrate object 
migrate = Migrate()
def creat_app()->Flask :
    app = Flask(__name__)
    login_manager.init_app(app)
    socketio.init_app(app , cors_allowed_origins="*")

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