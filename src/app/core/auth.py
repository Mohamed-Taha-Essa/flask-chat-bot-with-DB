from flask_login import LoginManager
from app.models import User
from app.db.database import SessionLocal


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == int(user_id)).first()
    db.close()
    return user