# models.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base

class Expense(Base):
    __tablename__ = "categorized_expenses"
    __table_args__ = {"extend_existing": True}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String,  nullable=False)
    category: Mapped[str] = mapped_column(String,  nullable=False)
    cost: Mapped[float] = mapped_column(Float,   nullable=False)
    
class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    limit: Mapped[float] = mapped_column(Float, nullable=False)

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

class Savings(Base):
    __tablename__ = "savings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    time_saved: Mapped[float] = mapped_column(Float, nullable=False)
    time_saved_unit: Mapped[str] = mapped_column(String, nullable=False)
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    rate_type: Mapped[str] = mapped_column(String, nullable=False)
    rate_time_unit: Mapped[str] = mapped_column(String, nullable=False)

