from app import db
from app.model_expense import Expense
from app.model_expense import expense_from_dict
from app.model_tag import Tag
from app.model_tag import tag_from_dict
from app.model_expense_nature import Expense_Nature
from app.model_expense_nature import expense_nature_from_dict
from app.model_expense_frequency import Expense_Frequency
from app.model_expense_frequency import expense_frequency_from_dict
from app.model_expense_category import Expense_Category
from app.model_expense_category import expense_category_from_dict
from app.model_expense_subcategory import Expense_Subcategory
from app.model_expense_subcategory import expense_subcategory_from_dict
import app.service_expense_classification_category as excc_sv
import app.service_expense_classification_nature as excn_sv
import app.service_expense_classification_frequency as excf_sv

from app.date_utils import to_date
from app.model_expense import to_dict
from app.date_utils import to_str_from_datetime
from app.date_utils import calc_month_key
import datetime
import statistics as stats
from dateutil.relativedelta import *

FORMATTED_OUTPUT_KEY = "formatted_output"
DAILY_EXPENSE_VALUES_KEY = "daily_expense_values"



def _convert_to_json_friendly_exp_agg(exp_aggr_tuple):
  return [to_str_from_datetime(exp_aggr_tuple.expense_date), float(exp_aggr_tuple.daily_expense)]

def _convert_to_json_friendly_exp_classication(exp_cat_tuple,prefix):
    return {prefix+"_name": exp_cat_tuple[0]
        , prefix+"_expenses": float(exp_cat_tuple[1])}
def _get_start_date(months_back):
  today = datetime.date.today()
  first = datetime.date(day=1, month=today.month, year=today.year)
  start = first+relativedelta(months=months_back)
  return start

def add_expense(expense_dict):
  expense = expense_from_dict(expense_dict)
  tags_data = expense_dict.get('tags', None)

  # TODO: Not sure if this belongs here or in the model class
  expense_nature = expense_nature_from_dict({'name': expense_dict.get('nature')})
  expense.nature = expense_nature

  expense_frequency = expense_frequency_from_dict({'name': expense_dict.get('frequency')})
  expense.frequency = expense_frequency

  expense_category = expense_category_from_dict({'name': expense_dict.get('category')})
  expense.category = expense_category

  expense_subcategory = expense_subcategory_from_dict({'name':expense_dict.get('subcategory')})
  expense.subcategory = expense_subcategory

  if tags_data is not None:
    for tag_data in tags_data:
      tag = tag_from_dict(tag_data)
      if tag is not None:
        expense.add_tag(tag)
  db.session.add(expense)
  db.session.commit()
  return to_dict(expense)

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
    monthly_data_output = {"key": month_key.split(":")[1], "values": daily_monthwise_expenses[month_key][FORMATTED_OUTPUT_KEY]}
    output.append(monthly_data_output)
    summaries.append({"month": month_key.split(":")[1], "summary": _calc_summary_obj(daily_monthwise_expenses[month_key][DAILY_EXPENSE_VALUES_KEY])})


  # daily_expense_values = month_value["daily_expense_values"]
  return output, summaries

def _calc_summary_obj(daily_expense_values_for_a_month):
  # NOTE: Works with 3.4 stats package. Might not work for 2.7
  summary = {}
  summary["Mean"] = "{0:.2f}".format(stats.mean(daily_expense_values_for_a_month))
  summary["Total"] = "{0:.2f}".format(sum(daily_expense_values_for_a_month))
  summary["Median"] = "{0:.2f}".format(stats.median(daily_expense_values_for_a_month))
  summary["Maximum"] = "{0:.2f}".format(max(daily_expense_values_for_a_month))
  summary["Minimum"] = "{0:.2f}".format(min(daily_expense_values_for_a_month))
  return summary

def _convert_daily_expense_to_month_wise(daily_expenses_tuple_list):

  daily_monthwise_expenses = {}

  def _get_month_value():
    month_value = daily_monthwise_expenses.get(month_key,None)
    if month_value == None:
      daily_monthwise_expenses[month_key] = {FORMATTED_OUTPUT_KEY:[],DAILY_EXPENSE_VALUES_KEY:[]}
      month_value = daily_monthwise_expenses[month_key]
    return month_value

  for daily_expense_tup in daily_expenses_tuple_list:
    month_key = _calc_month_key(daily_expense_tup)
    month_value = _get_month_value()
    month_value[FORMATTED_OUTPUT_KEY].append(_convert_to_json_friendly_exp_agg(daily_expense_tup))
    month_value[DAILY_EXPENSE_VALUES_KEY].append(daily_expense_tup.daily_expense)
  return daily_monthwise_expenses

def _calc_month_key(daily_expense_tup):
  """Creates a month key which has month number in front so that it can be sorted in ascending order of month"""
  return calc_month_key(daily_expense_tup.expense_date)

def get_expense_aggregates(period):
  st_date = _get_start_date(-6)
  daily_expenses_tuple_list = db.session.query(
    Expense.expense_date, db.func.sum(Expense.amount).label("daily_expense")).filter(Expense.expense_date>=st_date).group_by(
      Expense.expense_date).order_by(Expense.expense_date).all()
  if period=="daily":
    return calc_daily_expense_aggregates(daily_expenses_tuple_list)
  if period=="dailyMonthWise":
    return calc_daily_expense_aggregates_month_wise(daily_expenses_tuple_list)

def get_expense_aggregates_for_classification(classificationType):
  if classificationType=="category":
      category_expenses_tuple_list = db.session.query(
          Expense_Category.name.label("category"), db.func.sum(Expense.amount).label("category_expenses")).join(Expense).group_by(
              Expense_Category.id).order_by(db.desc("category_expenses")).all()
      cat_expenses = []
      for cat_expense_tup in category_expenses_tuple_list:
          cat_expenses.append(_convert_to_json_friendly_exp_classication(cat_expense_tup,"category"))
      return cat_expenses
  elif classificationType=="subcategory":
      subcategory_expenses_tuple_list = db.session.query(
          Expense_Subcategory.name.label("subcategory"), db.func.sum(Expense.amount).label("subcategory_expenses")).join(Expense).group_by(
              Expense_Subcategory.id).order_by(db.desc("subcategory_expenses")).all()
      subcat_expenses = []
      for subcat_expense_tup in subcategory_expenses_tuple_list:
          subcat_expenses.append(_convert_to_json_friendly_exp_classication(subcat_expense_tup,"subcategory"))
      return subcat_expenses

def get_expense_aggregates_for_classification_with_split(classificationType, split):
  if classificationType=="category":
    return excc_sv.get(split)
  elif classificationType=="nature":
    return excn_sv.get()
  elif classificationType=="frequency":
    return excf_sv.get()
