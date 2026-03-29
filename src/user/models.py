from sqlalchemy import Column , Integer , String 
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"
    id = Column(Integer , primary_key=True , index=True)
    name = Column(String)
    username = Column(String , unique=True , index=True , nullable=False)
    email = Column(String , unique=True , index=True)
    hash_password = Column(String , nullable=False)