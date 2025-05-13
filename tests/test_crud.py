from backend import schemas, crud

def test_expense_crud_lifecycle(db_session):
    # CREATE
    exp_in = schemas.ExpenseCreate(name="Coffee", cost=3.5)
    created = crud.create_expense(db_session, exp_in)
    assert created.name == "Coffee"
    assert created.cost == 3.5

    # READ
    all_exps = crud.get_expenses(db_session)
    assert len(all_exps) == 1

    # DELETE
    deleted = crud.delete_expense(db_session, created.id)
    assert deleted is True

    # VERIFY GONE
    assert crud.get_expenses(db_session) == []
