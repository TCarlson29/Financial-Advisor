# backend/crud.py
from sqlalchemy.orm import Session
from backend import models, schemas
from sqlalchemy import func, cast, String, Float

def get_expenses(
    db: Session,
    name: str | None = None,
    category: str | None = None,
    cost_min: float | None = None,
    cost_max: float | None = None,
):
    q = db.query(models.Expense)

    if name:
        q = q.filter(models.Expense.name.ilike(f"%{name}%"))
    if category:
        q = q.filter(models.Expense.category.ilike(f"%{category}%"))
    if cost_min is not None:
        q = q.filter(models.Expense.cost >= cost_min)
    if cost_max is not None:
        q = q.filter(models.Expense.cost <= cost_max)

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

def get_savings(
    db: Session,
    name:            str | None = None,
    time_saved_unit: str | None = None,
    rate_time_unit:  str | None = None,
    rate_type:       str | None = None,

    amount_min:      float | None = None,
    amount_max:      float | None = None,
    time_saved_min:  float | None = None,
    time_saved_max:  float | None = None,
    rate_min:        float | None = None,
    rate_max:        float | None = None,
    final_min:       float | None = None,
    final_max:       float | None = None,
    gain_min:        float | None = None,
    gain_max:        float | None = None,
) -> list[models.Savings]:
    q = db.query(models.Savings)

    # string fields → case-insensitive substring
    if name:
        q = q.filter(models.Savings.name.ilike(f"%{name}%"))
    if time_saved_unit:
        q = q.filter(models.Savings.time_saved_unit.ilike(f"%{time_saved_unit}%"))
    if rate_time_unit:
        q = q.filter(models.Savings.rate_time_unit.ilike(f"%{rate_time_unit}%"))
    if rate_type:
        q = q.filter(models.Savings.rate_type.ilike(f"%{rate_type}%"))

    # numeric ranges → >= / <=
    if amount_min is not None:
        q = q.filter(models.Savings.amount >= amount_min)
    if amount_max is not None:
        q = q.filter(models.Savings.amount <= amount_max)

    if time_saved_min is not None:
        q = q.filter(models.Savings.time_saved >= time_saved_min)
    if time_saved_max is not None:
        q = q.filter(models.Savings.time_saved <= time_saved_max)

    if rate_min is not None:
        q = q.filter(models.Savings.rate >= rate_min)
    if rate_max is not None:
        q = q.filter(models.Savings.rate <= rate_max)

    # final & gain are stored as strings, so cast to float for numeric comparison
    if final_min is not None:
        q = q.filter(cast(models.Savings.final, Float) >= final_min)
    if final_max is not None:
        q = q.filter(cast(models.Savings.final, Float) <= final_max)

    if gain_min is not None:
        q = q.filter(cast(models.Savings.gain, Float) >= gain_min)
    if gain_max is not None:
        q = q.filter(cast(models.Savings.gain, Float) <= gain_max)

    return q.all()

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