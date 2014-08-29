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


def _convert_to_json_friendly_exp_agg(exp_aggr_tuple):
  return [to_str_from_datetime(exp_aggr_tuple.expense_date), float(exp_aggr_tuple.daily_expense)]

def _convert_to_json_friendly_exp_classication(exp_cat_tuple,prefix):
    return {prefix+"_name": exp_cat_tuple[0]
        , prefix+"_expenses": float(exp_cat_tuple[1])}

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

def get_expense_aggregates(period):
  daily_expenses_tuple_list = db.session.query(
    Expense.expense_date, db.func.sum(Expense.amount).label("daily_expense")).group_by(
      Expense.expense_date).order_by(Expense.expense_date).all()
  daily_expenses = []
  for daily_expense_tup in daily_expenses_tuple_list:
    daily_expenses.append(_convert_to_json_friendly_exp_agg(daily_expense_tup))
  return daily_expenses

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

