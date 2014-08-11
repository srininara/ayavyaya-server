""" Will hold the tag model and also the many to many table connecting it to expense """
from app import db

tags = db.Table('expenses_tags',
  db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
  db.Column('expense_id', db.Integer, db.ForeignKey('expense.id')),
)

class Tag(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200))

  def __init__(self, name):
    self.name = name


def to_dict(tag):
    out = {}
    out['id'] = tag.id
    out['name'] = tag.name
    return out


def tag_from_dict(the_dict):
  id = the_dict.get('id', -1)
  name = the_dict.get('name', "")
  if id != -1:
    tag = Tag.query.get(id)
    return tag
  elif name != "":
    tag = Tag.query.filter_by(name=name).first()
    if tag is None:
      tag = Tag(name)
    return tag
  else:
    return None



  return Expense(description = the_dict.get('description', ''),
                expense_date = to_date(the_dict.get('expense_date','')),
                amount = the_dict.get('amount', 0))
