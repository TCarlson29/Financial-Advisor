# backend/routers/savings.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import cast, String

from backend import crud, schemas, models
from backend.database import get_db

router = APIRouter(
    prefix="/api/savings",
    tags=["savings"],
)

@router.get("/", response_model=List[schemas.SavingsRead])
def read_savings(db: Session = Depends(get_db)):
    return crud.get_savings(db)

@router.post("/", response_model=schemas.SavingsRead)
def create_savings(
    s: schemas.SavingsCreate,
    db: Session = Depends(get_db),
):
    return crud.create_savings(db, s)

@router.delete("/{s_id}", status_code=204)
def delete_savings(
    s_id: int,
    db: Session = Depends(get_db),
):
    if not crud.delete_savings(db, s_id):
        raise HTTPException(404, "Savings not found")
