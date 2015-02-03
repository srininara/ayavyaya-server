from app import db
from app.model.model_expense import Expense
from app.model.model_expense_category import Expense_Category
from app.model.model_expense_subcategory import Expense_Subcategory


def get_daily_expenses(start_date, end_date):
    return db.session.query(
        Expense.expense_date, db.func.sum(Expense.amount).label("daily_expense")).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).group_by(
        Expense.expense_date).order_by(Expense.expense_date).all()


def get_expenses_with_category_info(start_date, end_date):
    return db.session.query(Expense.amount.label("expense"),
                            Expense_Category.name.label("category"),
                            Expense_Subcategory.name.label("sub_category")).join(
        Expense_Category, Expense_Category.id == Expense.category_id).join(
        Expense_Subcategory, Expense_Subcategory.id == Expense.subcategory_id).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).all()


def get_expenses(start_date, no_of_recs):
    return db.session.query(Expense).filter(Expense.expense_date <= start_date).order_by(
        Expense.expense_date.desc()).limit(no_of_recs).all()