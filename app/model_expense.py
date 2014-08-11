from app import db
from app.api_inputs import to_date
from app.api_inputs import to_str_from_datetime
from app.model_tag import tags
from app.model_tag import to_dict as tag_as_dict
class Expense(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  description = db.Column(db.String(200))
  expense_date = db.Column(db.DateTime())
  amount = db.Column(db.Numeric(12,2))
  expense_tags = db.relationship('Tag', secondary=tags, backref=db.backref('expenses', lazy='dynamic'))

  def __init__(self, description, expense_date, amount):
    self.description = description
    self.expense_date = expense_date
    self.amount = amount

  def add_tag(self, tag):
    self.expense_tags.append(tag)

def expense_from_dict(the_dict):
  return Expense(description = the_dict.get('description', ''),
                expense_date = to_date(the_dict.get('expense_date','')),
                amount = the_dict.get('amount', 0))

def to_dict(expense):
    out = {}
    out['id'] = expense.id
    out['description'] = expense.description
    out['expense_date'] = to_str_from_datetime(expense.expense_date)
    out['amount'] = str(expense.amount)
    tagsOutput = []
    for tag in expense.expense_tags:
      tagsOutput.append(tag_as_dict(tag))
    out['tags'] = tagsOutput
    return out
