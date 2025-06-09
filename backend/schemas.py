# schemas.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional

class ExpenseCreate(BaseModel):
    name: str
    category: str
    cost: float

class ExpenseRead(ExpenseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ExpenseUpdate(BaseModel):
    name: str
    category: str
    cost: float

    class Config:
        orm_mode = True
    
class BudgetBase(BaseModel):
    category: str
    limit: float

class BudgetCreate(BudgetBase): ...
class BudgetRead(BudgetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
        
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase): ...
class CategoryRead(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SavingsBase(BaseModel):
    name: str
    amount: float
    time_saved: float
    time_saved_unit: str
    rate: float
    rate_time_unit: str
    rate_type: str
    final: str 
    gain: str 
    
class SavingsCreate(SavingsBase): ...
class SavingsRead(SavingsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SavingsUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    time_saved: Optional[float] = None
    time_saved_unit: Optional[str] = None
    rate: Optional[float] = None
    rate_time_unit: Optional[str] = None
    rate_type: Optional[str] = None
    final: Optional[str] = None
    gain: Optional[str] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)