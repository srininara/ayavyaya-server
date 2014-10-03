from app import db
from app.model_expense import Expense
from app.model_expense_category import Expense_Category
from app.model_expense_category import expense_category_from_dict
from toolz.itertoolz import *
from app.date_utils import calc_month_key


def _get_cat_split_for_each_month(cat_dw_exp_with_mth_tuple_list):
  cat_expense_mth_groupings = groupby(lambda tup: tup[3],cat_dw_exp_with_mth_tuple_list)
  month_summaries = {}
  for month in sorted(cat_expense_mth_groupings):
    month_summaries[month] = reduceby(lambda tup:tup[0],lambda acc,tup : acc + tup[2],cat_expense_mth_groupings[month],0)


# def get(split):
#   if split:
#     category_datewise_expenses_tuple_list = db.session.query(
#       Expense_Category.name.label("category"),Expense.expense_date,db.func.sum(Expense.amount).label("category_expenses")).join(Expense).group_by(
#           Expense_Category.id).group_by(Expense.expense_date).order_by(Expense.expense_date).order_by(db.asc("category")).all()
#
#     cat_dw_exp_with_mth_tuple_list = list((cat_tuple.category,cat_tuple.expense_date,float(cat_tuple.category_expenses),calc_month_key(cat_tuple.expense_date)) for cat_tuple in category_datewise_expenses_tuple_list)
#     cat_expense_mth_groupings = groupby(lambda tup: tup[3],cat_dw_exp_with_mth_tuple_list)
#     output = []
#     for month in sorted(cat_expense_mth_groupings):
#       output_rec = {"key": month.split(":")[1]}
#       cat_summary = (reduceby(lambda tup:tup[0],lambda acc,tup : acc + tup[2],cat_expense_mth_groupings[month],0))
#       out_value = []
#       for cat in sorted(cat_summary):
#         out_value.append([cat,cat_summary[cat]])
#       output_rec["values"] = out_value
#       output.append(output_rec)
#     return output



def get(split):
  if split:
    category_datewise_expenses_tuple_list = db.session.query(
      Expense_Category.name.label("category"),Expense.expense_date,db.func.sum(Expense.amount).label("category_expenses")).join(Expense).group_by(
          Expense_Category.id).group_by(Expense.expense_date).order_by(Expense.expense_date).order_by(db.asc("category")).all()

    cat_dw_exp_with_mth_tuple_list = list((cat_tuple.category,cat_tuple.expense_date,float(cat_tuple.category_expenses),calc_month_key(cat_tuple.expense_date)) for cat_tuple in category_datewise_expenses_tuple_list)
    cat_expense_groupings = groupby(lambda tup: tup[0],cat_dw_exp_with_mth_tuple_list)
    output = []
    for cat in sorted(cat_expense_groupings):
      output_rec = {"key": cat}
      cat_summary = (reduceby(lambda tup:tup[3],lambda acc,tup : acc + tup[2],cat_expense_groupings[cat],0))
      out_value = []
      for month in sorted(cat_summary):
        out_value.append([month.split(":")[0],cat_summary[month]])
      output_rec["values"] = out_value
      output.append(output_rec)
    return output



# for month_key in sorted(daily_monthwise_expenses):
#   monthly_data_output = {"key": month_key.split(":")[1], "values": daily_monthwise_expenses[month_key][FORMATTED_OUTPUT_KEY]}
#   output.append(monthly_data_output)
#   summaries.append({"month": month_key.split(":")[1], "summary": _calc_summary_obj(daily_monthwise_expenses[month_key][DAILY_EXPENSE_VALUES_KEY])})



    # category_dict = {}
    # for category_datewise_expense in category_datewise_expenses_tuple_list:
    #   category = category_datewise_expense.category
    #   if category_dict.get(category,None) == None:
    #     category_dict[category] = {}
    #   category_list = category_dict[category]
    #   if category_list.get(_get_)
