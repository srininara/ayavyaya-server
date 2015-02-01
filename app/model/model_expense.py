from app import db
from app.date_utils import to_date
from app.date_utils import to_str_from_datetime
from app.model.model_tag import tags
from app.model.model_tag import to_dict as tag_as_dict
from app.model.model_expense_nature import to_dict as nature_as_dict
from app.model.model_expense_frequency import to_dict as frequency_as_dict
from app.model.model_expense_category import to_dict as category_as_dict
from app.model.model_expense_subcategory import to_dict as subcategory_as_dict


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    expense_date = db.Column(db.DateTime())
    amount = db.Column(db.Numeric(12, 2))

    category_id = db.Column(db.Integer, db.ForeignKey('expense_category.id'))
    category = db.relationship('Expense_Category')

    subcategory_id = db.Column(db.Integer, db.ForeignKey('expense_subcategory.id'))
    subcategory = db.relationship('Expense_Subcategory')

    nature_id = db.Column(db.Integer, db.ForeignKey('expense_nature.id'))
    nature = db.relationship('Expense_Nature')

    frequency_id = db.Column(db.Integer, db.ForeignKey('expense_frequency.id'))
    frequency = db.relationship('Expense_Frequency')

    expense_tags = db.relationship('Tag', secondary=tags, backref=db.backref('expenses', lazy='dynamic'))

    def __init__(self, description, expense_date, amount):
        self.description = description
        self.expense_date = expense_date
        self.amount = amount

    def add_tag(self, tag):
        self.expense_tags.append(tag)


def expense_from_dict(the_dict):
    return Expense(description=the_dict.get('description', ''),
                   expense_date=to_date(the_dict.get('expense_date', '')),
                   amount=the_dict.get('amount', 0))


def to_dict(expense):
    out = {}
    out['id'] = expense.id
    out['description'] = expense.description
    out['expense_date'] = to_str_from_datetime(expense.expense_date)
    out['amount'] = str(expense.amount)

    nature_output = nature_as_dict(expense.nature)
    frequency_output = frequency_as_dict(expense.frequency)
    category_output = category_as_dict(expense.category)
    subcategory_output = subcategory_as_dict(expense.subcategory)

    out['nature_id'] = nature_output['id']
    out['nature'] = nature_output['name']

    out['frequency_id'] = frequency_output['id']
    out['frequency'] = frequency_output['name']

    out['category_id'] = category_output['id']
    out['category'] = category_output['name']

    out['subcategory_id'] = subcategory_output['id']
    out['subcategory'] = subcategory_output['name']

    tagsOutput = []
    for tag in expense.expense_tags:
        tagsOutput.append(tag_as_dict(tag))
    out['tags'] = tagsOutput
    return out
