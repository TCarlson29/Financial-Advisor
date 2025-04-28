# schemas.py
from pydantic import BaseModel

class ActivityCreate(BaseModel):
    name: str
    amount: float

class ActivityRead(ActivityCreate):
    id: int
    class Config:
        orm_mode = True
