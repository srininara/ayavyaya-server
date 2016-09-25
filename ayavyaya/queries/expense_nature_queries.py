from ayavyaya import db
from ayavyaya.model.model_expense_nature import ExpenseNature


def get_nat_listing():
    """Returns expense nature listing"""
    nature_tuples = db.session.query(ExpenseNature.id.label("id"),
                                     ExpenseNature.name.label("nature"),
                                     ExpenseNature.description.label("description")).all()
    return map(lambda x: {"id": x[0], "name": x[1], "description": x[2]}, nature_tuples)
