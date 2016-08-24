""" Will hold the expense subcategory model and also the reference to expense category """
from ayavyaya import db

DEFAULT_NOT_AVAILABLE_ID = - 1000
class Expense_Subcategory(db.Model):
    __tablename__ = 'expense_subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))

    category_id = db.Column(db.Integer, db.ForeignKey('expense_category.id'))
    category = db.relationship('Expense_Category')


    def __init__(self, name, description):
        self.name = name
        self.description = description


def to_dict(expense_subcategory):
    out = {}
    if expense_subcategory:
        out['id'] = expense_subcategory.id
        out['name'] = expense_subcategory.name
        out['description'] = expense_subcategory.description
    return out


def expense_subcategory_from_dict(the_dict):
    id = the_dict.get('id', DEFAULT_NOT_AVAILABLE_ID)
    name = the_dict.get('name', "")
    description = the_dict.get('description', "")
    if id and id != DEFAULT_NOT_AVAILABLE_ID:
        exp_subcategory = Expense_Subcategory.query.get(id)
        return exp_subcategory
    elif name:
        exp_subcategory = Expense_Subcategory.query.filter_by(name=name).first()
        if exp_subcategory is None:
            raise ValueError("Can't find a sub category with this name: ")
        return exp_subcategory
    else:
        expense_nature = Expense_Subcategory.query.get(DEFAULT_NOT_AVAILABLE_ID)
        return expense_nature
