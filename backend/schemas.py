# schemas.py
from pydantic import BaseModel, ConfigDict

class ActivityCreate(BaseModel):
    name: str
    amount: float

class ActivityRead(ActivityCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
