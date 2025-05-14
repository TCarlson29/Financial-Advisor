# crud.py
from sqlalchemy.orm import Session
from backend import models, schemas

def get_expenses(db: Session):
    return db.query(models.Expense).all()

def create_expense(db: Session, exp: schemas.ExpenseCreate):
    db_exp = models.Expense(name=exp.name, cost=exp.cost)
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

def delete_expense(db: Session, exp_id: int) -> bool:
    obj = db.get(models.Expense, exp_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
