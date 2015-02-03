from app import db
from app.model.model_expense_frequency import Expense_Frequency

def get_freq_listing():
    return db.session.query(Expense_Frequency.name.label("frequency")).all()

