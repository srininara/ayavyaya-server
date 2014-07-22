from json import dumps
from app import db
from app.api_inputs import to_date
from app.api_inputs import to_str_from_datetime
class Expense(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  description = db.Column(db.String(200))
  expense_date = db.Column(db.DateTime())
  amount = db.Column(db.Numeric(12,2))

  def __init__(self, description, expense_date, amount):
    self.description = description
    self.expense_date = expense_date
    self.amount = amount

def expense_from_dict(the_dict):
  return Expense(description = the_dict.get('description', ''),
                expense_date = to_date(the_dict.get('expense_date','')),
                amount = the_dict.get('amount', 0))

def to_dict(model):
    out = {}
    out['id'] = model.id
    out['description'] = model.description
    out['expense_date'] = to_str_from_datetime(model.expense_date)
    out['amount'] = str(model.amount)
    return out
