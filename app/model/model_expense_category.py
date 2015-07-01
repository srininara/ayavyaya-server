""" Will hold the expense category model """
from app import db


class Expense_Category(db.Model):
    __tablename__ = 'expense_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))

    def __init__(self, name, description):
        self.name = name
        self.description = description


def to_dict(expense_category):
    out = {}
    if expense_category:
        out['id'] = expense_category.id
        out['name'] = expense_category.name
        out['description'] = expense_category.description
    return out


def expense_category_from_dict(the_dict):
    id = the_dict.get('id', -1)
    name = the_dict.get('name', "")
    description = the_dict.get('description', "")
    if id and id != -1:
        exp_category = Expense_Category.query.get(id)
        return exp_category
    elif name and name != "":
        exp_category = Expense_Category.query.filter_by(name=name).first()
        if exp_category is None:
            raise ValueError("Can't find a category with this name")
        return exp_category
