# schemas.py
from pydantic import BaseModel, ConfigDict

class ExpenseCreate(BaseModel):
    name: str
    category: str
    cost: float

class ExpenseRead(ExpenseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
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
    final: float 
    gain: float 
    
class SavingsCreate(SavingsBase): ...
class SavingsRead(SavingsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)