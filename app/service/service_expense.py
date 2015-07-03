import datetime

from dateutil.relativedelta import *
import elasticsearch

from app import db
from app.model.model_expense import Expense
from app.model.model_expense import expense_from_dict
from app.date_utils import to_date


# from app.model.model_expense import to_dict
from app.model.model_tag import tag_from_dict
from app.model.model_expense_nature import expense_nature_from_dict
from app.model.model_expense_frequency import expense_frequency_from_dict
from app.model.model_expense_category import Expense_Category
from app.model.model_expense_category import expense_category_from_dict
from app.model.model_expense_subcategory import Expense_Subcategory
from app.model.model_expense_subcategory import expense_subcategory_from_dict
import app.service.service_expense_classification_category as excc_sv
import app.service.service_expense_classification_nature as excn_sv
import app.service.service_expense_classification_frequency as excf_sv
import app.service.daily_expense_aggregator as dagg
from app.model.model_expense import to_dict
from app.date_utils import to_str_from_datetime
from app.queries import expense_queries as eq

es = elasticsearch.Elasticsearch()

def _convert_to_json_friendly_exp_agg(exp_aggr_tuple):
    return [to_str_from_datetime(exp_aggr_tuple.expense_date), float(exp_aggr_tuple.daily_expense)]


def _convert_to_json_friendly_exp_classication(exp_cat_tuple, prefix):
    return {prefix + "_name": exp_cat_tuple[0]
        , prefix + "_expenses": float(exp_cat_tuple[1])}


def _get_start_date(months_back):
    today = datetime.date.today()
    first = datetime.date(day=1, month=today.month, year=today.year)
    start = first + relativedelta(months=months_back)
    return start

def _add_to_es(committed_expense_dict=None):
    es.index(index='ayavyaya', doc_type='expense', id=committed_expense_dict.get('id'), body=committed_expense_dict)

def add_expense(expense_dict):
    expense = expense_from_dict(expense_dict)
    tags_data = expense_dict.get('tags', None)

    # TODO: Not sure if this belongs here or in the model class

    expense_nature = expense_nature_from_dict({'name': expense_dict.get('nature'), 'id': expense_dict.get('nature_id')})
    expense.nature = expense_nature

    expense_frequency = expense_frequency_from_dict(
        {'name': expense_dict.get('frequency'), 'id': expense_dict.get('frequency_id')})
    expense.frequency = expense_frequency

    expense_category = expense_category_from_dict(
        {'name': expense_dict.get('category'), 'id': expense_dict.get('category_id')})
    expense.category = expense_category

    expense_subcategory = expense_subcategory_from_dict(
        {'name': expense_dict.get('subcategory'), 'id': expense_dict.get('subcategory_id')})
    expense.subcategory = expense_subcategory

    if tags_data is not None:
        for tag_data in tags_data:
            tag = tag_from_dict(tag_data)
            if tag is not None:
                expense.add_tag(tag)
    db.session.add(expense)
    db.session.commit()
    committed_expense_dict = to_dict(expense)

    _add_to_es(committed_expense_dict)
    return committed_expense_dict

def update_expense(id, expense_dict):
    upd_exp = Expense.query.get(id)
    upd_exp.description = expense_dict.get("description", upd_exp.description)
    exp_date = expense_dict.get("expense_date")
    upd_exp.expense_date = to_date(exp_date) if exp_date else upd_exp.expense_date
    upd_exp.amount = expense_dict.get("amount", upd_exp.amount)

    tags_data = expense_dict.get('tags', None)

    # TODO: Not sure if this belongs here or in the model class

    expense_nature = expense_nature_from_dict({'name': expense_dict.get('nature'), 'id': expense_dict.get('nature_id')})
    upd_exp.nature = expense_nature

    expense_frequency = expense_frequency_from_dict(
        {'name': expense_dict.get('frequency'), 'id': expense_dict.get('frequency_id')})
    upd_exp.frequency = expense_frequency

    expense_category = expense_category_from_dict(
        {'name': expense_dict.get('category'), 'id': expense_dict.get('category_id')})
    upd_exp.category = expense_category

    expense_subcategory = expense_subcategory_from_dict(
        {'name': expense_dict.get('subcategory'), 'id': expense_dict.get('subcategory_id')})
    upd_exp.subcategory = expense_subcategory

    if tags_data is not None:
        for tag_data in tags_data:
            tag = tag_from_dict(tag_data)
            if tag is not None:
                upd_exp.add_tag(tag)
    db.session.commit()
    committed_expense_dict = to_dict(upd_exp)
    _add_to_es(committed_expense_dict)
    return committed_expense_dict


def get_expenses():
    expenses = eq.get_expenses(datetime.datetime.now(), 20)
    expense_dict_list = []
    for expense in expenses:
        expense_dict = to_dict(expense)
        expense_dict_list.append(expense_dict)
    return expense_dict_list


def get_expense_aggregates(period):
    return dagg.get_daily_aggregates(period)


def get_expense_aggregates_for_classification(classificationType):
    if classificationType == "category":
        category_expenses_tuple_list = db.session.query(
            Expense_Category.name.label("category"), db.func.sum(Expense.amount).label("category_expenses")).join(
            Expense).group_by(
            Expense_Category.id).order_by(db.desc("category_expenses")).all()
        cat_expenses = []
        for cat_expense_tup in category_expenses_tuple_list:
            cat_expenses.append(_convert_to_json_friendly_exp_classication(cat_expense_tup, "category"))
        return cat_expenses
    elif classificationType == "subcategory":
        subcategory_expenses_tuple_list = db.session.query(
            Expense_Subcategory.name.label("subcategory"),
            db.func.sum(Expense.amount).label("subcategory_expenses")).join(Expense).group_by(
            Expense_Subcategory.id).order_by(db.desc("subcategory_expenses")).all()
        subcat_expenses = []
        for subcat_expense_tup in subcategory_expenses_tuple_list:
            subcat_expenses.append(_convert_to_json_friendly_exp_classication(subcat_expense_tup, "subcategory"))
        return subcat_expenses


def get_expense_aggregates_for_classification_with_split(classificationType, split):
    if classificationType == "category":
        return excc_sv.get(split)
    elif classificationType == "nature":
        return excn_sv.get()
    elif classificationType == "frequency":
        return excf_sv.get()


