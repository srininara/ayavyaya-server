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


from app.api_inputs import to_date
from app.model_expense import to_dict
from app.api_inputs import to_str_from_datetime


def _convert_to_json_friendly_arr_rec(exp_aggr_tuple):
  return [to_str_from_datetime(exp_aggr_tuple.expense_date),float(exp_aggr_tuple.daily_expense)]
  # exp_aggr_dict["expense_date"] = to_str_from_datetime(exp_aggr_tuple.expense_date)
  # exp_aggr_dict["daily_expense"] = str(exp_aggr_tuple.daily_expense)
  # return exp_aggr_dict

def add_expense(expense_dict):
  expense = expense_from_dict(expense_dict)
  tags_data = expense_dict.get('tags',None)

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

def get_expense_aggregates(period):
  daily_expenses_tuple_list = db.session.query(
    Expense.expense_date,db.func.sum(Expense.amount).label("daily_expense")).group_by(
      Expense.expense_date).order_by(Expense.expense_date).all()
  daily_expenses = []
  for daily_expense_tup in daily_expenses_tuple_list:
    daily_expenses.append(_convert_to_json_friendly_arr_rec(daily_expense_tup))
  return daily_expenses
