# crud.py
from sqlalchemy.orm import Session
from backend import models, schemas

def get_expenses(db: Session, search: str | None = None):
    q = db.query(models.Expense)
    if search:
        q = q.filter(models.Expense.name.ilike(f"%{search}%"))
    return q.all()

def create_expense(db: Session, exp: schemas.ExpenseCreate):
    db_exp = models.Expense(name=exp.name, category =exp.category, cost=exp.cost)
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

def get_budgets(db: Session) -> list[models.Budget]:
    return db.query(models.Budget).all()

def upsert_budget(db: Session, b: schemas.BudgetCreate) -> models.Budget:
    obj = db.query(models.Budget).filter_by(category=b.category).first()
    if obj:
        obj.limit = b.limit
    else:
        obj = models.Budget(**b.model_dump())
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, c: schemas.CategoryCreate):
    db_c = models.Category(name=c.name)
    db.add(db_c)
    db.commit()
    db.refresh(db_c)
    return db_c

def delete_category(db: Session, c_id: int) -> bool:
    obj = db.get(models.Category, c_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def get_savings(db: Session) -> list[models.Savings]:
    return db.query(models.Savings).all()

def create_savings(db: Session, s: schemas.SavingsCreate) -> models.Savings:
    db_savings = models.Savings(**s.model_dump())
    db.add(db_savings)
    db.commit()
    db.refresh(db_savings)
    return db_savings

def delete_savings(db: Session, s_id: int) -> bool:
    obj = db.get(models.Savings, s_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True