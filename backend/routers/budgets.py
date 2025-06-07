# backend/routers/budgets.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/api/budgets",
    tags=["budgets"],
)

@router.get("/", response_model=List[schemas.BudgetRead])
def read_budgets(db: Session = Depends(get_db)):
    return crud.get_budgets(db)

@router.post("/", response_model=schemas.BudgetRead)
def upsert_budget(
    bud: schemas.BudgetCreate,
    db: Session = Depends(get_db),
):
    return crud.upsert_budget(db, bud)
