# main.py
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(  # same CORS as before
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

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
    




