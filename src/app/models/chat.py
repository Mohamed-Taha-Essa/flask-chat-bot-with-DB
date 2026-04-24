"""
this file for create chatsession models to store the chat session between user and llm in database
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.db.database import Base


class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_name = Column(String(100), nullable=False)
    question = Column(Text , nullable=True)
    responses = Column(Text, nullable=False)  # Store the chat history as a JSON string


    created_at = Column(DateTime, default=func.now())

    user = relationship('User', backref='chat_sessions')