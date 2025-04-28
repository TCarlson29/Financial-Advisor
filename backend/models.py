# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Activity(Base):
    __tablename__ = "activities"
    id     = Column(Integer, primary_key=True, index=True)
    name   = Column(String,  nullable=False)
    amount = Column(Float,   nullable=False)
