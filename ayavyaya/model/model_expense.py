from ayavyaya import db
from ayavyaya.date_utils import to_date
from ayavyaya.date_utils import to_str_from_datetime
from ayavyaya.date_utils import to_iso_str_from_datetime
from ayavyaya.model.model_tag import tags
from ayavyaya.model.model_tag import to_dict as tag_as_dict
from ayavyaya.model.model_expense_nature import to_dict as nature_as_dict
from ayavyaya.model.model_expense_category import to_dict as category_as_dict
from ayavyaya.model.model_expense_subcategory import to_dict as subcategory_as_dict

expense_tag_xref = db.Table('expenses_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('expense_id', db.Integer, db.ForeignKey('expense.id')), extend_existing=True
)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    expense_date = db.Column(db.DateTime())
    last_modified_date = db.Column(db.DateTime())
    amount = db.Column(db.Numeric(12, 2))

    category_id = db.Column(db.Integer, db.ForeignKey('expense_category.id'))
    category = db.relationship('ExpenseCategory')

    subcategory_id = db.Column(db.Integer, db.ForeignKey('expense_subcategory.id'))
    subcategory = db.relationship('ExpenseSubcategory')

    nature_id = db.Column(db.Integer, db.ForeignKey('expense_nature.id'))
    nature = db.relationship('ExpenseNature')

    expense_tags = db.relationship('Tag', secondary=expense_tag_xref, backref=db.backref('expenses', lazy='dynamic'))

    def __init__(self, description, expense_date, amount):
        self.description = description
        self.expense_date = expense_date
        self.amount = amount

    def add_tag(self, tag):
        self.expense_tags.append(tag)

    def remove_all_tags(self):
        self.expense_tags[:] = []


def expense_from_dict(the_dict):
    return Expense(description=the_dict.get('description', ''),
                   expense_date=to_date(the_dict.get('expense_date', '')),
                   amount=the_dict.get('amount', 0))


def to_dict(expense):
    out = {'id': expense.id, 'description': expense.description,
           'expense_date': to_str_from_datetime(expense.expense_date)}
    if expense.last_modified_date:
        out['last_modified_date'] = to_iso_str_from_datetime(expense.last_modified_date)
    # out['amount'] = str(expense.amount)
    out['amount'] = float(expense.amount)

    nature_output = nature_as_dict(expense.nature)
    category_output = category_as_dict(expense.category)
    subcategory_output = subcategory_as_dict(expense.subcategory)

    if nature_output:
        out["nature"] = nature_output

    if category_output:
        out["category"] = category_output

    if subcategory_output:
        out["subcategory"] = subcategory_output

    tags_output = []
    for tag in expense.expense_tags:
        tags_output.append(tag_as_dict(tag))
    out['tags'] = tags_output
    return out
