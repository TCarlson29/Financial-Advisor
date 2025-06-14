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
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="substring match in name"),
    category: Optional[str] = Query(None, description="substring match in category"),
    cost_min: Optional[float] = Query(None, alias="cost_min"),
    cost_max: Optional[float] = Query(None, alias="cost_max"),
):
    return crud.get_expenses(db, name, category, cost_min, cost_max)

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

@router.put("/{exp_id}", response_model=schemas.ExpenseRead)
def update_expense(
    exp_id: int,
    exp: schemas.ExpenseUpdate,  # Make sure you have this schema defined
    db: Session = Depends(get_db),
):
    updated_expense = crud.update_expense(db, exp_id, exp)
    if not updated_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated_expense