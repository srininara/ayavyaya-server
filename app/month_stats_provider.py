__author__ = 'srininara'

import functools as ft

import numpy as np
import toolz.itertoolz as itz

from app import db
from app.model_expense import Expense
from app.model_expense_category import Expense_Category
from app.model_expense_subcategory import Expense_Subcategory
from app.date_utils import *


def _money_format(value):
    return "{0:.2f}".format(value)


def _calc_daily_expenses_summary_obj(daily_expense_values_for_a_month):
    summary = {"mean": _money_format(np.mean(daily_expense_values_for_a_month)),
               "total": _money_format(sum(daily_expense_values_for_a_month)),
               "median": _money_format(np.median(daily_expense_values_for_a_month)),
               "maximum": _money_format(max(daily_expense_values_for_a_month)),
               "minimum": _money_format(min(daily_expense_values_for_a_month)),
               "lower_quartile": _money_format(np.percentile(daily_expense_values_for_a_month, 25)),
               "upper_quartile": _money_format(np.percentile(daily_expense_values_for_a_month, 75))}
    return summary


def dailyData(month_identifier):
    start_date = to_first_day_from_mth_str(month_identifier)
    end_date = add_a_month_to(start_date)
    daily_expenses_tuple_list = db.session.query(
        Expense.expense_date, db.func.sum(Expense.amount).label("daily_expense")).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).group_by(
        Expense.expense_date).order_by(Expense.expense_date).all()
    daily_values = [{"expense_date": to_str_from_datetime(expense_date), "daily_expense": float(daily_expense)} for
                    expense_date, daily_expense in daily_expenses_tuple_list]
    summary = _calc_daily_expenses_summary_obj([x["daily_expense"] for x in daily_values])
    return daily_values, summary


def categoryData(month_identifier):
    start_date = to_first_day_from_mth_str(month_identifier)
    end_date = add_a_month_to(start_date)

    exp_list_with_full_category_info = db.session.query(Expense.amount.label("expense"),
                                                        Expense_Category.name.label("category"),
                                                        Expense_Subcategory.name.label("sub_category")).join(
        Expense_Category, Expense_Category.id == Expense.category_id).join(
        Expense_Subcategory, Expense_Subcategory.id == Expense.subcategory_id).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).all()

    exp_list_grouped_by_category = itz.groupby(lambda tup: tup[1], exp_list_with_full_category_info)

    output = []
    for category in sorted(exp_list_grouped_by_category):
        category_data = exp_list_grouped_by_category[category]
        category_rec = {"category": category, "category_expenses": float(ft.reduce(lambda exp, tup: exp + tup[0],
                                                                                   category_data, 0)),
                        "sub_categories": []}
        cat_exp_list_grouped_by_sub_category = itz.groupby(lambda tup: tup[2], category_data)
        for sub_category in sorted(cat_exp_list_grouped_by_sub_category):
            sub_category_data = cat_exp_list_grouped_by_sub_category[sub_category]
            sub_category_rec = {"sub_category": sub_category,
                                "sub_category_expenses": float(ft.reduce(lambda exp, tup: exp + tup[0],
                                                                         sub_category_data, 0))}
            category_rec["sub_categories"].append(sub_category_rec)
            output.append(category_rec)

    return output


# def categoryData(month_identifier):
# start_date = to_first_day_from_mth_str(month_identifier)
# end_date = add_a_month_to(start_date)
#
# category_expenses_tuple_list = db.session.query(
# Expense_Category.name.label("category"),
# db.func.sum(Expense.amount).label("category_expenses")).join(Expense).filter(
# Expense.expense_date >= start_date, Expense.expense_date < end_date).group_by(
# Expense_Category.id).order_by(db.asc("category")).all()
# category_values = [{"category": category, "category_expenses": float(category_expenses)} for
#                        category, category_expenses in category_expenses_tuple_list]
#     summary = []
#     return category_values, summary

