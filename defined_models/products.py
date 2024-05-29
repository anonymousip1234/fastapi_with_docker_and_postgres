from sqlalchemy import Column,Integer,String,Float
from databases import Base

class Products(Base):

    __tablename__ = 'products'

    id = Column(Integer,primary_key=True)
    name = Column(String,index=True)
    category = Column(String)
    price = Column(Float)
