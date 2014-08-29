""" Will hold the expense nature model """
from app import db


class Expense_Nature(db.Model):
  __tablename__ = 'expense_nature'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  description = db.Column(db.String(300))

  def __init__(self, name, description):
    self.name = name
    self.description = description


def to_dict(expense_nature):
    out = {}
    out['id'] = expense_nature.id
    out['name'] = expense_nature.name
    out['description'] = expense_nature.description
    return out


def expense_nature_from_dict(the_dict):
  id = the_dict.get('id', -1)
  name = the_dict.get('name', "")
  description = the_dict.get('description', "")
  if id != -1:
    expense_nature = Expense_Nature.query.get(id)
    return expense_nature
  elif name != "":
    expense_nature = Expense_Nature.query.filter_by(name=name).first()
    if expense_nature is None:
      raise ValueError("Can't find a nature with this name")
    return expense_nature
  else:
    raise ValueError("Need to provide name or id")
