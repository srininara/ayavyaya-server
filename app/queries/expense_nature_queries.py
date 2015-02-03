from app import db
from app.model.model_expense_nature import Expense_Nature

def get_nat_listing():
    return db.session.query(Expense_Nature.name.label("nature")).all()
