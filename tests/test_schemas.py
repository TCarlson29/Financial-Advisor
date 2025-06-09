# backend/tests/test_schemas.py
import pytest
from pydantic import ValidationError
from backend import schemas

def test_expense_schema_rejects_non_string_name():
    # name must be str, cost must be float
    with pytest.raises(ValidationError):
        schemas.ExpenseCreate(name=123, category="Miscellaneous", cost=5.0)

def test_expense_schema_rejects_non_numeric_cost():
    with pytest.raises(ValidationError):
        schemas.ExpenseCreate(name="Lunch", category="Food", cost="free")
