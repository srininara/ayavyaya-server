__author__ = 'srininara'
import datetime
import statistics as stats

from dateutil.relativedelta import *

from app import db
from app.model_expense import Expense
from app.date_utils import calc_month_key
from app.date_utils import to_str_from_datetime


FORMATTED_OUTPUT_KEY = "formatted_output"
DAILY_EXPENSE_VALUES_KEY = "daily_expense_values"


def _convert_to_json_friendly_exp_agg(exp_aggr_tuple):
    return [to_str_from_datetime(exp_aggr_tuple.expense_date), float(exp_aggr_tuple.daily_expense)]


def _get_start_date(months_back):
    today = datetime.date.today()
    first = datetime.date(day=1, month=today.month, year=today.year)
    start = first + relativedelta(months=months_back)
    return start


def _calc_summary_obj(daily_expense_values_for_a_month):
    # NOTE: Works with 3.4 stats package. Might not work for 2.7
    summary = {}
    summary["Mean"] = "{0:.2f}".format(stats.mean(daily_expense_values_for_a_month))
    summary["Total"] = "{0:.2f}".format(sum(daily_expense_values_for_a_month))
    summary["Median"] = "{0:.2f}".format(stats.median(daily_expense_values_for_a_month))
    summary["Maximum"] = "{0:.2f}".format(max(daily_expense_values_for_a_month))
    summary["Minimum"] = "{0:.2f}".format(min(daily_expense_values_for_a_month))
    return summary


def _calc_month_key(daily_expense_tup):
    """Creates a month key which has month number in front so that it can be sorted in ascending order of month"""
    return calc_month_key(daily_expense_tup.expense_date)


def _convert_daily_expense_to_month_wise(daily_expenses_tuple_list):
    daily_monthwise_expenses = {}

    def _get_month_value():
        month_value = daily_monthwise_expenses.get(month_key, None)
        if month_value == None:
            daily_monthwise_expenses[month_key] = {FORMATTED_OUTPUT_KEY: [], DAILY_EXPENSE_VALUES_KEY: []}
            month_value = daily_monthwise_expenses[month_key]
        return month_value

    for daily_expense_tup in daily_expenses_tuple_list:
        month_key = _calc_month_key(daily_expense_tup)
        month_value = _get_month_value()
        month_value[FORMATTED_OUTPUT_KEY].append(_convert_to_json_friendly_exp_agg(daily_expense_tup))
        month_value[DAILY_EXPENSE_VALUES_KEY].append(daily_expense_tup.daily_expense)
    return daily_monthwise_expenses


def calc_daily_expense_aggregates(daily_expenses_tuple_list):
    daily_expenses_output = []
    daily_expense_values = []
    for daily_expense_tup in daily_expenses_tuple_list:
        daily_expenses_output.append(_convert_to_json_friendly_exp_agg(daily_expense_tup))
        daily_expense_values.append(daily_expense_tup.daily_expense)

    summary = _calc_summary_obj(daily_expense_values)
    return daily_expenses_output, summary


def calc_daily_expense_aggregates_month_wise(daily_expenses_tuple_list):
    daily_monthwise_expenses = _convert_daily_expense_to_month_wise(daily_expenses_tuple_list)
    output = []
    summaries = []
    for month_key in sorted(daily_monthwise_expenses):
        monthly_data_output = {"key": month_key.split(":")[1],
                               "values": daily_monthwise_expenses[month_key][FORMATTED_OUTPUT_KEY]}
        output.append(monthly_data_output)
        summaries.append({"month": month_key.split(":")[1],
                          "summary": _calc_summary_obj(daily_monthwise_expenses[month_key][DAILY_EXPENSE_VALUES_KEY])})


    # daily_expense_values = month_value["daily_expense_values"]
    return output, summaries


def get_daily_aggregates(period):
    st_date = _get_start_date(-6)
    daily_expenses_tuple_list = db.session.query(
        Expense.expense_date, db.func.sum(Expense.amount).label("daily_expense")).filter(
        Expense.expense_date >= st_date).group_by(
        Expense.expense_date).order_by(Expense.expense_date).all()
    if period == "daily":
        return calc_daily_expense_aggregates(daily_expenses_tuple_list)
    if period == "dailyMonthWise":
        return calc_daily_expense_aggregates_month_wise(daily_expenses_tuple_list)
    if period == "dailyMonthWiseStat":
        # dummy implementation
        return [[850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960,
                 850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960,
                 850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960,
                 850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960,
                 850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960,
                 850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960,
                 960], [960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760,
                        960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760,
                        960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760,
                        960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760,
                        960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760,
                        960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760,
                        800], [880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850, 840,
                               880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850, 840,
                               840, 880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850,
                               840,
                               840, 880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850,
                               840,
                               840, 880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850,
                               840,
                               840, 880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850,
                               840,
                               840,
                               840, 840], [890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910, 920, 890, 860, 880,
                                           720, 840, 850, 850, 890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910,
                                           920, 890, 860, 880,
                                           720, 840, 850, 850, 890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910,
                                           920, 890, 860, 880,
                                           720, 840, 850, 850, 890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910,
                                           920, 890, 860, 880,
                                           720, 840, 850, 850, 890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910,
                                           920, 890, 860, 880,
                                           720, 840, 850, 850, 890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910,
                                           920, 890, 860, 880,
                                           720, 840, 850, 850, 780], [890, 840, 780, 810, 760, 810, 790, 810, 820, 850,
                                                                      870, 870, 810, 740, 810, 940, 950, 800, 810, 890,
                                                                      840, 780, 810, 760, 810, 790, 810, 820, 850,
                                                                      870, 870, 810, 740, 810, 940, 950, 800, 810, 890,
                                                                      840, 780, 810, 760, 810, 790, 810, 820, 850,
                                                                      870, 870, 810, 740, 810, 940, 950, 800, 810, 890,
                                                                      840, 780, 810, 760, 810, 790, 810, 820, 850,
                                                                      870, 870, 810, 740, 810, 940, 950, 800, 810, 890,
                                                                      840, 780, 810, 760, 810, 790, 810, 820, 850,
                                                                      870, 870, 810, 740, 810, 940, 950, 800, 810, 890,
                                                                      840, 780, 810, 760, 810, 790, 810, 820, 850,
                                                                      870, 870, 810, 740, 810, 940, 950, 800, 810,
                                                                      870]], []
