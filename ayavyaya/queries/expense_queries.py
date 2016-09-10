from ayavyaya import db
from ayavyaya.model.model_expense import Expense
from ayavyaya.model.model_expense_category import ExpenseCategory
from ayavyaya.model.model_expense_subcategory import ExpenseSubcategory


def get_daily_expenses(start_date, end_date):
    return db.session.query(
        Expense.expense_date, db.func.sum(Expense.amount).label("daily_expense")).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).group_by(
        Expense.expense_date).order_by(Expense.expense_date).all()


def get_expenses_with_category_info(start_date, end_date):
    return db.session.query(Expense.amount.label("expense"),
                            ExpenseCategory.name.label("category"),
                            ExpenseSubcategory.name.label("sub_category")).join(
        ExpenseCategory, ExpenseCategory.id == Expense.category_id).join(
        ExpenseSubcategory, ExpenseSubcategory.id == Expense.subcategory_id).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).all()


def get_expenses(start_date, start_index, no_of_recs):
    return db.session.query(Expense).filter(Expense.expense_date <= start_date).order_by(
        Expense.expense_date.desc(), Expense.id.desc()).offset(start_index).limit(no_of_recs).all()
