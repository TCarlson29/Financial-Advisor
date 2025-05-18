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
    class Config:
        orm_mode = True

