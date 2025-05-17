# models.py
from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Expense(Base):
    __tablename__ = "categorized_expenses"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  nullable=False)
    category = Column(String,  nullable=False)
    cost = Column(Float,   nullable=False)
