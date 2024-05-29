from sqlalchemy import Boolean,Column,Integer,String
from databases import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True,index=True)
    email = Column(String)
    password = Column(String)