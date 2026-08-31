from sqlalchemy import Column,String,Integer,VARCHAR,ForeignKey
from database import Base

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String(225))
    email = Column(String(225), unique=True)
    password = Column(String(225))
