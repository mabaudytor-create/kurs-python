from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Client(Base):
    __tablename__ = "klienci"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

class Order(Base):
    __tablename__ = "zamowienia"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer)
    amount = Column(Float)

