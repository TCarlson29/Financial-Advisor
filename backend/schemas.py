from pydantic import BaseModel

class TaskCreate(BaseModel):
    text: str

class TaskRead(TaskCreate):
    id: int

    class Config:
        orm_mode = True
