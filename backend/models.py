from sqlalchemy import Column, Integer, String
from .database import Base
from datetime import datetime
from sqlalchemy import DateTime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    score = Column(Integer)
    total = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

