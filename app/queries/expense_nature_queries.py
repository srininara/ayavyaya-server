from app import db
from app.model.model_expense_nature import Expense_Nature


def get_nat_listing():
    nature_tuples = db.session.query(Expense_Nature.id.label("id"),
                                     Expense_Nature.name.label("nature"),
                                     Expense_Nature.description.label("description")).all()
    return map(lambda x: {"id": x[0], "name": x[1], "description": x[2]}, nature_tuples)
