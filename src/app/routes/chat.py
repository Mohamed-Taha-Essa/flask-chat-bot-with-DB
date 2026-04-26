from flask import Blueprint ,render_template ,request 
from flask_login import login_required ,current_user
from app.db.database import get_db_session 
from app.models import User
from app.extensions import socketio
from .ai import initialize_sql_agent 

chat_bp = Blueprint('chat' , __name__, template_folder='templates' )

@chat_bp.route('/chat')
@login_required
def chat():
    return render_template('chat/chat.html' , username=current_user.username)

@login_required
@socketio.on('message')
def handle_message(data):
  
    agent = initialize_sql_agent(current_user.roles)
    print('role:' ,current_user.roles)
    response = agent.invoke({"input": data})
    print(response)
    socketio.emit('message' , {'response' : response['output']})