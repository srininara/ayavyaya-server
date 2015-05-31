from app import db
from app.model.model_expense_frequency import Expense_Frequency


def get_freq_listing():
    frequency_tuples = db.session.query(
        Expense_Frequency.id.label("id"),
        Expense_Frequency.name.label("frequency"),
        Expense_Frequency.description.label("description")
    ).all()
    return map(lambda x: {"id": x[0], "name": x[1], "description": x[2]}, frequency_tuples)
