# models.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base

class Expense(Base):
    __tablename__ = "categorized_expenses"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  nullable=False)
    category = Column(String,  nullable=False)
    cost = Column(Float,   nullable=False)
    
class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    limit: Mapped[float] = mapped_column(Float, nullable=False)

