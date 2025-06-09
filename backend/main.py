# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from backend.database import engine, Base, get_db, SessionLocal
from backend.routers import expenses, budgets, categories, savings
from backend.models import Category, Expense, Savings
from contextlib import asynccontextmanager

# Create tables
Base.metadata.create_all(bind=engine)



@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        # default categories
        defaults = ["Food", "Transport", "Entertainment", "Utilities", "Miscellaneous"]
        for name in defaults:
            try:
                db.add(Category(name=name))
                db.commit()
            except IntegrityError:
                db.rollback()

        # default expenses
        if db.query(Expense).count() == 0:
            default_expenses = [
                {"name": "Coffee",      "category": "Food",          "cost": 3.50},
                {"name": "Monthly Metro","category": "Transport",    "cost": 50.00},
                {"name": "Movie Ticket", "category": "Entertainment","cost": 12.00},
            ]
            for e in default_expenses:
                db.add(Expense(**e))
            db.commit()

        # default savings
        if db.query(Savings).count() == 0:
            default_savings = [
                {
                    "name": "Emergency Fund",
                    "amount": 1000.0,
                    "time_saved": 6,
                    "time_saved_unit": "Month",     # from timeUnits
                    "rate": 1.5,
                    "rate_time_unit": "Year",       # from timeUnits
                    "rate_type": "Simple",          # from rateTypes
                    "final": 1000.0,                # amount + (amount * rate% * (6/12))
                    "gain": 0.0,
                },
                {
                    "name": "Vacation",
                    "amount": 2000.0,
                    "time_saved": 1,
                    "time_saved_unit": "Year",
                    "rate": 2.0,
                    "rate_time_unit": "Year",
                    "rate_type": "Compound",
                    "final": 2040.0,                # 2000 * (1 + 0.02)^1
                    "gain": 40.0,
                },
                {
                    "name": "Car Down Payment",
                    "amount": 500.0,
                    "time_saved": 12,
                    "time_saved_unit": "Month",
                    "rate": 1.0,
                    "rate_time_unit": "Year",
                    "rate_type": "Compound",
                    "final": 505.0,                 # 500 * (1 + 0.01)^(12/12)
                    "gain": 5.0,
                },
            ]

            for s in default_savings:
                db.add(Savings(**s))
            db.commit()

        yield

    finally:
        db.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount routers
app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(categories.router)
app.include_router(savings.router)