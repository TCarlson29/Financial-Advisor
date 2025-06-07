# backend/routers/categories.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud, schemas, models
from backend.database import get_db

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
)

@router.get("/", response_model=List[schemas.CategoryRead])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@router.post("/", response_model=schemas.CategoryRead)
def create_category(
    cat: schemas.CategoryCreate,
    db: Session = Depends(get_db),
):
    return crud.create_category(db, cat)

@router.delete("/{cat_id}", status_code=204)
def delete_category(
    cat_id: int,
    db: Session = Depends(get_db),
):
    if not crud.delete_category(db, cat_id):
        raise HTTPException(404, "Category not found")
