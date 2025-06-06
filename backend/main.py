# main.py
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend import crud, models, schemas, database
from backend.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware( 
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.on_event("startup")
def seed_default_categories():
    db = SessionLocal()
    defaults = ["Food", "Transport", "Entertainment", "Utilities", "Miscellaneous"]
    for name in defaults:
        try:
            # try insert; if unique constraint fails, ignore
            db.add(models.Category(name=name))
            db.commit()
        except IntegrityError:
            db.rollback()
    db.close()

@app.get("/api/expenses", response_model=list[schemas.ExpenseRead])
def read_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)

@app.post("/api/expenses", response_model=schemas.ExpenseRead)
def create_expense(act: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, act)

@app.delete("/api/expenses/{exp_id}", status_code=204)
def delete_expense(exp_id: int, db: Session = Depends(get_db)):
    if not crud.delete_expense(db, exp_id):
        raise HTTPException(status_code=404, detail="Expense not found")

@app.get("/api/budgets", response_model=list[schemas.BudgetRead])
def read_budgets(db: Session = Depends(get_db)):
    return crud.get_budgets(db)

@app.post("/api/budgets", response_model=schemas.BudgetRead)
def create_or_update_budget(bud: schemas.BudgetCreate, db: Session = Depends(get_db)):
    return crud.upsert_budget(db, bud)

@app.get("/api/categories", response_model=list[schemas.CategoryRead])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@app.post("/api/categories", response_model=schemas.CategoryRead)
def create_category(cat: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, cat)

@app.delete("/api/categories/{cat_id}", status_code=204)
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    if not crud.delete_category(db, cat_id):
        raise HTTPException(status_code=404, detail="Category not found")

@app.get("/api/savings", response_model=list[schemas.SavingsRead])
def read_savings(db: Session = Depends(get_db)):
    return crud.get_savings(db)

@app.post("/api/savings", response_model=schemas.SavingsRead)
def create_savings(s: schemas.SavingsCreate, db: Session = Depends(get_db)):
    return crud.create_savings(db, s)

@app.delete("/api/savings/{s_id}", status_code=204)
def delete_savings(s_id: int, db: Session = Depends(get_db)):
    if not crud.delete_savings(db, s_id):
        raise HTTPException(status_code=404, detail="Savings not found")



