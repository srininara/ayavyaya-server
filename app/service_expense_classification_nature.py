from toolz.itertoolz import *

from app import db
from app.model.model_expense import Expense
from app.model.model_expense_nature import Expense_Nature
from app.date_utils import calc_month_key


def get():
    nature_datewise_expenses_tuple_list = db.session.query(
        Expense_Nature.name.label("nature"), Expense.expense_date,
        db.func.sum(Expense.amount).label("nature_expenses")).join(Expense).group_by(
        Expense_Nature.id).group_by(Expense.expense_date).order_by(Expense.expense_date).order_by(
        db.asc("nature")).all()

    nat_dw_exp_with_mth_tuple_list = [(nat_tuple.nature, nat_tuple.expense_date,
                                       float(nat_tuple.nature_expenses), calc_month_key(nat_tuple.expense_date))
                                      for nat_tuple in nature_datewise_expenses_tuple_list]
    nat_expense_groupings = groupby(lambda tup: tup[0], nat_dw_exp_with_mth_tuple_list)
    output = []
    for nat in sorted(nat_expense_groupings):
        output_rec = {"key": nat}
        nat_summary = (reduceby(lambda tup: tup[3], lambda acc, tup: acc + tup[2], nat_expense_groupings[nat], 0))
        out_value = []
        for month in sorted(nat_summary):
            out_value.append([month.split(":")[0], nat_summary[month]])
        output_rec["values"] = out_value
        output.append(output_rec)
    return output
