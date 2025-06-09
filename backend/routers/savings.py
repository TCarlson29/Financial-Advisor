# backend/routers/savings.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import cast, String

from backend import crud, schemas, models
from backend.database import get_db

from decimal import Decimal

router = APIRouter(
    prefix="/api/savings",
    tags=["savings"],
)

@router.get("/", response_model=List[schemas.SavingsRead])
def list_savings(
    db: Session                = Depends(get_db),

    # string filters
    name:            Optional[str] = Query(None, description="substring match on plan name"),
    time_saved_unit: Optional[str] = Query(None, description="substring match on time unit"),
    rate_time_unit:  Optional[str] = Query(None, description="substring match on rate time unit"),
    rate_type:       Optional[str] = Query(None, description="substring match on rate type"),

    # numeric ranges
    amount_min:      Optional[float] = Query(None, description="minimum amount saved"),
    amount_max:      Optional[float] = Query(None, description="maximum amount saved"),
    time_saved_min:  Optional[float] = Query(None, alias="time_saved_min", description="min saving duration"),
    time_saved_max:  Optional[float] = Query(None, alias="time_saved_max", description="max saving duration"),
    rate_min:        Optional[float] = Query(None, description="minimum rate (%)"),
    rate_max:        Optional[float] = Query(None, description="maximum rate (%)"),
    final_min:       Optional[float] = Query(None, alias="final_min", description="min final amount"),
    final_max:       Optional[float] = Query(None, alias="final_max", description="max final amount"),
    gain_min:        Optional[float] = Query(None, alias="gain_min", description="min gain"),
    gain_max:        Optional[float] = Query(None, alias="gain_max", description="max gain"),
):
    return crud.get_savings(
        db,
        name=name,
        time_saved_unit=time_saved_unit,
        rate_time_unit=rate_time_unit,
        rate_type=rate_type,
        amount_min=amount_min,
        amount_max=amount_max,
        time_saved_min=time_saved_min,
        time_saved_max=time_saved_max,
        rate_min=rate_min,
        rate_max=rate_max,
        final_min=final_min,
        final_max=final_max,
        gain_min=gain_min,
        gain_max=gain_max,
    )

@router.post("/", response_model=schemas.SavingsRead)
def create_savings(
    s: schemas.SavingsCreate,
    db: Session = Depends(get_db),
):
    return crud.create_savings(db, s)

@router.put("/{saving_id}", response_model=schemas.SavingsRead)
def update_saving(
    saving_id: int,
    saving: schemas.SavingsUpdate,  # Make sure you have this schema defined
    db: Session = Depends(get_db),
):
    updated_saving = crud.update_saving(db, saving_id, saving)
    if not updated_saving:
        raise HTTPException(status_code=404, detail="Saving not found")
    return updated_saving

@router.delete("/{s_id}", status_code=204)
def delete_savings(
    s_id: int,
    db: Session = Depends(get_db),
):
    if not crud.delete_savings(db, s_id):
        raise HTTPException(404, "Savings not found")
