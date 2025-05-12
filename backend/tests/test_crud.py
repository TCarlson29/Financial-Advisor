import schemas, crud

def test_create_and_get_activity(db_session):
    # db_session is from our fixture, backed by :memory:
    item_in = schemas.ExpenseCreate(name="Coffee", cost=3.5)
    created = crud.create_expense(db_session, item_in)
    all_ = crud.get_expenses(db_session)
    assert len(all_) == 1
    assert all_[0].name == "Coffee"
