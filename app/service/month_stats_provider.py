__author__ = 'srininara'

import functools as ft

import numpy as np
import toolz.itertoolz as itz


from app import db
from app.model.model_expense import Expense
from app.queries import expense_queries as eq
from app.queries import expense_category_queries as ecq
from app.date_utils import *

tolerance_limit = 5


def _money_format(value):
    return "{0:.2f}".format(value)


def _find_start_end_dates(month_identifier):
    start_date = to_first_day_from_mth_str(month_identifier)
    end_date = add_a_month_to(start_date)
    return end_date, start_date


def _calc_daily_expenses_summary_obj(daily_expense_values_for_a_month):
    summary = {}
    if daily_expense_values_for_a_month:
        summary = {"mean": _money_format(np.mean(daily_expense_values_for_a_month)),
                   "total": _money_format(sum(daily_expense_values_for_a_month)),
                   "median": _money_format(np.median(daily_expense_values_for_a_month)),
                   "maximum": _money_format(max(daily_expense_values_for_a_month)),
                   "minimum": _money_format(min(daily_expense_values_for_a_month)),
                   "lower_quartile": _money_format(np.percentile(daily_expense_values_for_a_month, 25)),
                   "upper_quartile": _money_format(np.percentile(daily_expense_values_for_a_month, 75))}
    return summary

def _compare(curr_value, prev_value, tolerance_limit):
    min_value = prev_value * (1 - (tolerance_limit / 100.0))
    max_value = prev_value * (1 + (tolerance_limit / 100.0))
    return "Decreased" if curr_value < min_value else "Increased" if curr_value > max_value else "In Limit"


def _calc_comparison(summary, prev_month_summary):
    comparison_attributes = ["maximum", "mean", "median"]
    if summary and prev_month_summary:
        return {x: _compare(float(summary[x]), float(prev_month_summary[x]), tolerance_limit) for x in
                comparison_attributes}
    else:
        return {}


def daily_stats(month_identifier):
    # Behavior note: Even when data for the criteria is not found, the method empty shells
    end_date, start_date = _find_start_end_dates(month_identifier)
    prev_month_start_date = prev_month_to(start_date)
    daily_expenses_tuple_list = eq.get_daily_expenses(start_date, end_date)
    prev_daily_expenses_tuple_list = eq.get_daily_expenses(prev_month_start_date, start_date)

    daily_values = [{"expense_date": to_str_from_datetime(expense_date), "daily_expense": float(daily_expense)} for
                    expense_date, daily_expense in daily_expenses_tuple_list]
    summary = _calc_daily_expenses_summary_obj([x["daily_expense"] for x in daily_values])

    prev_month_summary = _calc_daily_expenses_summary_obj([float(x) for _, x in prev_daily_expenses_tuple_list])

    comparison = _calc_comparison(summary, prev_month_summary)

    return daily_values, summary, prev_month_summary, comparison


def category_stats(month_identifier):
    # Behavior note: Even when data for the criteria is not found, the method empty shells
    end_date, start_date = _find_start_end_dates(month_identifier)
    prev_month_start_date = prev_month_to(start_date)

    exp_list_with_full_category_info = eq.get_expenses_with_category_info(start_date, end_date)
    prev_month_exp_list_with_full_category_info = eq.get_expenses_with_category_info(prev_month_start_date, start_date)
    raw_cat_listing = ecq.get_cat_sub_cat_listing()

    cat_list_grouped_by_category = itz.groupby(lambda tup: tup[0], raw_cat_listing)
    exp_list_grouped_by_category = itz.groupby(lambda tup: tup[1], exp_list_with_full_category_info)
    prev_month_exp_list_grouped_by_category = itz.groupby(lambda tup: tup[1],
                                                          prev_month_exp_list_with_full_category_info)

    output = []
    for category in sorted(cat_list_grouped_by_category):
        cat_list_raw = cat_list_grouped_by_category.get(category)
        cat_exp_raw = exp_list_grouped_by_category.get(category)
        prev_mth_cat_exp_raw = prev_month_exp_list_grouped_by_category.get(category)
        category_expenses = float(ft.reduce(lambda exp, tup: exp + tup[0], cat_exp_raw, 0)) if cat_exp_raw else 0
        prev_month_category_expenses = float(ft.reduce(lambda exp, tup: exp + tup[0], prev_mth_cat_exp_raw,
                                                       0)) if prev_mth_cat_exp_raw else 0
        category_comparison = _compare(category_expenses, prev_month_category_expenses, tolerance_limit)
        category_rec = {"category": category, "category_expenses": category_expenses,
                        "prev_month_category_expenses": prev_month_category_expenses,
                        "category_comparison": category_comparison,
                        "sub_categories": []}

        cat_list_grouped_by_sub_cat = itz.groupby(lambda tup: tup[1], cat_list_raw)
        cat_exp_list_grouped_by_sub_category = itz.groupby(lambda tup: tup[2], cat_exp_raw) if cat_exp_raw else {}
        prev_mth_cat_exp_list_grpd_by_sub_cat = itz.groupby(lambda tup: tup[2],
                                                            prev_mth_cat_exp_raw) if prev_mth_cat_exp_raw else {}

        for sub_category in sorted(cat_list_grouped_by_sub_cat):
            sub_category_data = cat_exp_list_grouped_by_sub_category.get(sub_category)
            prev_mth_sub_category_data = prev_mth_cat_exp_list_grpd_by_sub_cat.get(sub_category)
            sub_category_expenses = float(ft.reduce(lambda exp, tup: exp + tup[0],
                                                    sub_category_data, 0)) if sub_category_data else 0
            prev_month_sub_category_expenses = float(ft.reduce(lambda exp, tup: exp + tup[0],
                                                               prev_mth_sub_category_data,
                                                               0)) if prev_mth_sub_category_data else 0
            sub_category_comparison = _compare(sub_category_expenses, prev_month_sub_category_expenses, tolerance_limit)

            sub_category_rec = {"sub_category": sub_category,
                                "sub_category_expenses": sub_category_expenses,
                                "prev_month_sub_category_expenses": prev_month_sub_category_expenses,
                                "sub_category_comparison": sub_category_comparison}
            category_rec["sub_categories"].append(sub_category_rec)

        output.append(category_rec)
    return output


def top_expenses_stats(month_identifier):
    # Behavior note: Even when data for the criteria is not found, the method empty shells
    end_date, start_date = _find_start_end_dates(month_identifier)
    limit_val = 10
    top_expenses_by_value_raw_list = db.session.query(
        Expense.description, db.func.sum(Expense.amount).label("expense_amount"),
        db.func.count(Expense.amount).label("frequency")).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).group_by(
        Expense.description).order_by("expense_amount DESC").limit(limit_val).all()
    top_expenses_by_value_json_list = [
        {"description": description, "total_value": float(expense_amount), "frequency_spread": frequency} for
        description, expense_amount, frequency in top_expenses_by_value_raw_list]
    top_expenses_by_frequency_raw_list = db.session.query(
        Expense.description, db.func.sum(Expense.amount).label("expense_amount"),
        db.func.count(Expense.amount).label("frequency")).filter(
        Expense.expense_date >= start_date, Expense.expense_date < end_date).group_by(
        Expense.description).order_by("frequency DESC").limit(limit_val).all()
    top_expenses_by_frequency_json_list = [
        {"description": description, "total_value": float(expense_amount), "frequency_spread": frequency} for
        description, expense_amount, frequency in top_expenses_by_frequency_raw_list]
    return top_expenses_by_value_json_list, top_expenses_by_frequency_json_list
