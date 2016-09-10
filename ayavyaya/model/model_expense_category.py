""" Will hold the expense category model """
from ayavyaya import db

DEFAULT_NOT_AVAILABLE_ID = - 1000


class ExpenseCategory(db.Model):
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
    category_id = the_dict.get('id', DEFAULT_NOT_AVAILABLE_ID)
    name = the_dict.get('name', "")
    description = the_dict.get('description', "")
    if category_id and category_id != DEFAULT_NOT_AVAILABLE_ID:
        exp_category = ExpenseCategory.query.get(category_id)
        return exp_category
    elif name and name != "":
        exp_category = ExpenseCategory.query.filter_by(name=name).first()
        if exp_category is None:
            raise ValueError("Can't find a category with this name")
        return exp_category
    else:
        exp_category = ExpenseCategory.query.get(DEFAULT_NOT_AVAILABLE_ID)
        return exp_category

