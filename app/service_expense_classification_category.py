from toolz.itertoolz import *

from app import db
from app.model_expense import Expense
from app.model_expense_category import Expense_Category
from app.date_utils import calc_month_key


def get(split):
    if split:
        category_datewise_expenses_tuple_list = db.session.query(
            Expense_Category.name.label("category"), Expense.expense_date,
            db.func.sum(Expense.amount).label("category_expenses")).join(Expense).group_by(
            Expense_Category.id).group_by(Expense.expense_date).order_by(Expense.expense_date).order_by(
            db.asc("category")).all()

        cat_dw_exp_with_mth_tuple_list = [
            (cat_tuple.category, cat_tuple.expense_date, float(cat_tuple.category_expenses),
             calc_month_key(cat_tuple.expense_date))
            for cat_tuple in category_datewise_expenses_tuple_list]
        cat_expense_groupings = groupby(lambda tup: tup[0], cat_dw_exp_with_mth_tuple_list)
        output = []
        for cat in sorted(cat_expense_groupings):
            output_rec = {"key": cat}
            cat_summary = (reduceby(lambda tup: tup[3], lambda acc, tup: acc + tup[2], cat_expense_groupings[cat], 0))
            out_value = []
            for month in sorted(cat_summary):
                out_value.append([month.split(":")[0], cat_summary[month]])
            output_rec["values"] = out_value
            output.append(output_rec)
        return output
