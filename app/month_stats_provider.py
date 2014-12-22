__author__ = 'srininara'

import numpy as np
from app import db
from app.model_expense import Expense
from app.date_utils import *


def _money_format(value):
    return "{0:.2f}".format(value)

def _calc_summary_obj(daily_expense_values_for_a_month):
    summary = {"mean": _money_format(np.mean(daily_expense_values_for_a_month)),
               "total": _money_format(sum(daily_expense_values_for_a_month)),
               "median": _money_format(np.median(daily_expense_values_for_a_month)),
               "maximum": _money_format(max(daily_expense_values_for_a_month)),
               "minimum": _money_format(min(daily_expense_values_for_a_month)),
               "lower_quartile": _money_format(np.percentile(daily_expense_values_for_a_month, 25)),
               "upper_quartile": _money_format(np.percentile(daily_expense_values_for_a_month, 75))}
    return summary


def daily(month_identifier):
    start_date = to_first_day_from_mth_str(month_identifier)
    end_date = add_a_month_to(start_date)
    daily_expenses_tuple_list = db.session.query(
        Expense.expense_date, db.func.sum(Expense.amount).label("daily_expense")).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).group_by(
        Expense.expense_date).order_by(Expense.expense_date).all()
    daily_values = [{"expense_date": to_str_from_datetime(expense_date), "daily_expense": float(daily_expense)} for
                    expense_date, daily_expense in daily_expenses_tuple_list]
    summary = _calc_summary_obj([x["daily_expense"] for x in daily_values])
    return daily_values, summary

