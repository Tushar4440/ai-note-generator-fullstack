from sqlalchemy import Column, Integer, String, Text
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

class UserInput(Base):
    __tablename__ = "inputs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(Text)

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(Text)