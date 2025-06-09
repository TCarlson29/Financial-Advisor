from fastapi.testclient import TestClient
import pytest
from backend.main import app, get_db
from backend.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



def test_read_empty(client):
    response = client.get("/api/expenses")
    assert response.json() == []

def test_add_one(client):
    expense = {"name": "Sample", "category": "Food", "cost":17}
    r = client.post("/api/expenses", json=expense)
    assert r.status_code == 200 # OK
    
    response = client.get("/api/expenses")
    assert len(response.json()) == 1

def test_delete_empty(client):
    d = client.delete("/api/expenses/1")
    assert d.status_code == 404

def test_add_one_then_delete_it(client):
    expense = {"name": "Sample", "category": "Food", "cost":17}
    r = client.post("/api/expenses", json=expense)
    assert r.status_code == 200 # OK
    
    d = client.delete("/api/expenses/1")
    assert d.status_code == 204 # No Content
    
    response = client.get("/api/expenses")
    assert response.json() == []

def test_add_one_then_delete_other(client):
    expense = {"name": "Sample", "category": "Food", "cost":17}
    r = client.post("/api/expenses", json=expense)
    assert r.status_code == 200 # OK
    
    d = client.delete("/api/expenses/10")
    assert d.status_code == 404
    
def test_add_duplicate(client):
    expense = {"name": "Sample", "category": "Food", "cost":17}
    r1 = client.post("/api/expenses", json=expense)
    assert r1.status_code == 200 # OK
    
    r2 = client.post("/api/expenses", json=expense)
    assert r2.status_code == 200 # OK
    
    d1 = client.delete("/api/expenses/1")
    assert d1.status_code == 204
    
    d2 = client.delete("/api/expenses/2")
    assert d2.status_code == 204
    
    
@pytest.mark.parametrize("payload,field", [
    ({"cost":10.0, "category": "Food", "name":42}, "name"),
    ({"name":"Taxi", "category": "Food", "cost":"expensive"}, "cost"),
    ({"name":None, "category": "Food",  "cost":None}, "name"),
])
def test_create_expense_api_invalid_types(client, payload, field):
    r = client.post("/api/expenses", json=payload)
    assert r.status_code == 422, f"expected validation error on `{field}`, got {r.status_code}"
    data = r.json()
    assert data["detail"][0]["loc"][-1] == field