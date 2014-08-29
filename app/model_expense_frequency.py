""" Will hold the expense frequency model """
from app import db


class Expense_Frequency(db.Model):
  __tablename__ = 'expense_frequency'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  description = db.Column(db.String(300))

  def __init__(self, name, description):
    self.name = name
    self.description = description


def to_dict(expense_frequency):
    out = {}
    out['id'] = expense_frequency.id
    out['name'] = expense_frequency.name
    out['description'] = expense_frequency.description
    return out


def expense_frequency_from_dict(the_dict):
  id = the_dict.get('id', -1)
  name = the_dict.get('name', "")
  description = the_dict.get('description', "")
  if id != -1:
    expense_frequency = Expense_Frequency.query.get(id)
    return expense_frequency
  elif name != "":
    expense_frequency = Expense_Frequency.query.filter_by(name=name).first()
    if expense_frequency is None:
      raise ValueError("Can't find a frequency with this name")
    return expense_frequency
  else:
    raise ValueError("Need to provide name or id")
