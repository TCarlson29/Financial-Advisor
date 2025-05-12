# crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_expenses(db: Session):
    return db.query(models.Expense).all()

def create_expense(db: Session, act: schemas.ExpenseCreate):
    db_act = models.Expense(name=act.name, cost=act.cost)
    db.add(db_act)
    db.commit()
    db.refresh(db_act)
    return db_act

def delete_expense(db: Session, act_id: int):
    obj = db.query(models.Expense).get(act_id)
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
