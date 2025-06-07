# backend/routers/expenses.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/expenses",
    tags=["expenses"],
)

@router.get("/", response_model=List[schemas.ExpenseRead])
def list_expenses(
    search: Optional[str] = Query(None, description="name substring"),
    db: Session = Depends(get_db),
):
    return crud.get_expenses(db, search)

@router.post("/", response_model=schemas.ExpenseRead)
def create_expense(
    exp: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
):
    return crud.create_expense(db, exp)

@router.delete("/{exp_id}", status_code=204)
def delete_expense(
    exp_id: int,
    db: Session = Depends(get_db),
):
    if not crud.delete_expense(db, exp_id):
        raise HTTPException(404, "Expense not found")