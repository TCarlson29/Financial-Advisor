from sqlalchemy.orm import Session
import models, schemas

def get_tasks(db: Session):
    return db.query(models.Task).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(text=task.text)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    obj = db.query(models.Task).filter(models.Task.id == task_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
