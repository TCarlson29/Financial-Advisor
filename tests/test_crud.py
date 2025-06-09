from backend import schemas, crud
import pytest

def test_expense_crud_lifecycle(db_session):
    # CREATE
    exp_in = schemas.ExpenseCreate(name="Coffee", category="Food", cost=3.5)
    created = crud.create_expense(db_session, exp_in)
    assert created.name == "Coffee"
    assert created.category == "Food"
    assert created.cost == 3.5

    # READ
    all_exps = crud.get_expenses(db_session)
    assert len(all_exps) == 1

    # DELETE
    deleted = crud.delete_expense(db_session, created.id)
    assert deleted is True

    # VERIFY GONE
    assert crud.get_expenses(db_session) == []
    
def test_delete_nonexistent_expense(db_session):
    # deleting an ID that was never created should return False
    assert crud.delete_expense(db_session, 9999) is False

def test_create_multiple_and_read(db_session):
    # create several expenses in a row
    inputs = [
        schemas.ExpenseCreate(name="Breakfast", category="Food", cost=5.0),
        schemas.ExpenseCreate(name="Yoyo", category="Entertainment", cost=12.5),
        schemas.ExpenseCreate(name="Car", category="Transport", cost=20.0),
    ]
    created = [crud.create_expense(db_session, inp) for inp in inputs]

    # make sure the returned objects have the right data
    assert [e.name  for e in created] == ["Breakfast", "Yoyo", "Car"]
    assert [e.category  for e in created] == ["Food", "Entertainment", "Transport"]
    assert [e.cost  for e in created] == [5.0, 12.5, 20.0]

    # get_expenses should return all three
    all_exps = crud.get_expenses(db_session)
    assert len(all_exps) == 3
    names = {e.name for e in all_exps}
    assert names == {"Breakfast", "Yoyo", "Car"}

def test_delete_then_recreate(db_session):
    # create one
    tea = schemas.ExpenseCreate(name="Tea", category="Food", cost=3.0)
    first = crud.create_expense(db_session, tea)
    # delete it
    assert crud.delete_expense(db_session, first.id) is True
    # now create again with same data
    second = crud.create_expense(db_session, tea)
    assert second.name == "Tea"
    assert second.category == "Food"
    assert second.cost == 3.0

def test_session_isolation_between_tests(db_session):
    # this just confirms that db_session starts empty
    assert crud.get_expenses(db_session) == []

@pytest.mark.parametrize("name,category,cost", [
    ("Snack", "Food", 2.75),
    ("Gum","Food", 0.50),
    ("Book","Entertainment", 15.99),
])
def test_various_expenses(db_session, name, category, cost):
    exp_in = schemas.ExpenseCreate(name=name, category=category, cost=cost)
    exp = crud.create_expense(db_session, exp_in)
    assert exp.name == name
    assert exp.category == category
    assert exp.cost == cost
    # cleanup
    assert crud.delete_expense(db_session, exp.id) is True