from toolz.itertoolz import *

from app import db
from app.model_expense import Expense
from app.model_expense_frequency import Expense_Frequency
from app.date_utils import calc_month_key


def get():
    frequency_datewise_expenses_tuple_list = db.session.query(
        Expense_Frequency.name.label("frequency"), Expense.expense_date,
        db.func.sum(Expense.amount).label("frequency_expenses")).join(Expense).group_by(
        Expense_Frequency.id).group_by(Expense.expense_date).order_by(Expense.expense_date).order_by(
        db.asc("frequency")).all()

    fre_dw_exp_with_mth_tuple_list = [(fre_tuple.frequency, fre_tuple.expense_date,
                                       float(fre_tuple.frequency_expenses), calc_month_key(fre_tuple.expense_date))
                                      for fre_tuple in frequency_datewise_expenses_tuple_list]
    fre_expense_groupings = groupby(lambda tup: tup[0], fre_dw_exp_with_mth_tuple_list)
    output = []
    for nat in sorted(fre_expense_groupings):
        output_rec = {"key": nat}
        fre_summary = (reduceby(lambda tup: tup[3], lambda acc, tup: acc + tup[2], fre_expense_groupings[nat], 0))
        out_value = []
        for month in sorted(fre_summary):
            out_value.append([month.split(":")[0], fre_summary[month]])
        output_rec["values"] = out_value
        output.append(output_rec)
    return output

# There is a lot of repetition between this and nature and category monthwise classification. Need to make it better
