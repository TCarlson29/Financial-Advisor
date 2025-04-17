from sqlalchemy import Column, Integer, String 
from users_sample import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    nickname = Column(String)