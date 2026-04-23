from flask import Flask , jsonify
from flask_migrate import Migrate
from app.core.config import settings
 
# gobla migrate object 
migrate = Migrate()
def creat_app()->Flask :
    app = Flask(__name__)
    migrate.init_app(app , db= None, directory='migrations')

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
    app.run(
        host = settings.HOST,
        port = settings.PORT,
        debug = settings.DEBUG 
    )