# main.py
from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/api/activities", response_model=list[schemas.ActivityRead])
def read_activities(db: Session = Depends(get_db)):
    return crud.get_activities(db)

@app.post("/api/activities", response_model=schemas.ActivityRead)
def create_activity(act: schemas.ActivityCreate, db: Session = Depends(get_db)):
    return crud.create_activity(db, act)

@app.delete("/api/activities/{act_id}", status_code=204)
def delete_activity(act_id: int, db: Session = Depends(get_db)):
    if not crud.delete_activity(db, act_id):
        raise HTTPException(status_code=404, detail="Activity not found")
