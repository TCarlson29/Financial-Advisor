# schemas.py
from pydantic import BaseModel, ConfigDict

class ExpenseCreate(BaseModel):
    name: str
    category: str
    cost: float

class ExpenseRead(ExpenseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
