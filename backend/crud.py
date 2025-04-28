# crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_activities(db: Session):
    return db.query(models.Activity).all()

def create_activity(db: Session, act: schemas.ActivityCreate):
    db_act = models.Activity(name=act.name, amount=act.amount)
    db.add(db_act)
    db.commit()
    db.refresh(db_act)
    return db_act

def delete_activity(db: Session, act_id: int):
    obj = db.query(models.Activity).get(act_id)
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
