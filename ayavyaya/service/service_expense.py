import datetime

from dateutil.relativedelta import *
import elasticsearch

from ayavyaya import db
from ayavyaya.model.model_expense import Expense
from ayavyaya.model.model_expense import expense_from_dict
from ayavyaya.date_utils import to_date


# from app.model.model_expense import to_dict
from ayavyaya.model.model_tag import tag_from_dict
from ayavyaya.model.model_expense_nature import expense_nature_from_dict
from ayavyaya.model.model_expense_category import ExpenseCategory
from ayavyaya.model.model_expense_category import expense_category_from_dict
from ayavyaya.model.model_expense_subcategory import ExpenseSubcategory
from ayavyaya.model.model_expense_subcategory import expense_subcategory_from_dict
from ayavyaya.model.model_expense import to_dict
from ayavyaya.date_utils import to_str_from_datetime
from ayavyaya.date_utils import to_iso_date_from_str
from ayavyaya.queries import expense_queries as eq
from ayavyaya import app

log = app.logger

es = elasticsearch.Elasticsearch()


def _convert_to_json_friendly_exp_agg(exp_aggr_tuple):
    return [to_str_from_datetime(exp_aggr_tuple.expense_date), float(exp_aggr_tuple.daily_expense)]


def _convert_to_json_friendly_exp_classication(exp_cat_tuple, prefix):
    return {prefix + "_name": exp_cat_tuple[0], prefix + "_expenses": float(exp_cat_tuple[1])}


def _get_start_date(months_back):
    today = datetime.date.today()
    first = datetime.date(day=1, month=today.month, year=today.year)
    start = first + relativedelta(months=months_back)
    return start


def _add_to_es(committed_expense_dict=None):
    pass
    # es.index(index='ayavyaya', doc_type='expense', id=committed_expense_dict.get('id'), body=committed_expense_dict)


def validate(expense_dict):
    exp_date = expense_dict.get('expense_date', None)
    amount = expense_dict.get('amount', None)
    description = expense_dict.get('description', None)
    if not (exp_date and amount and description):
        raise ValueError("Expense Date, Amount and Description are mandatory")


def add_expense(expense_dict):
    validate(expense_dict)
    expense = expense_from_dict(expense_dict)
    # log.info(expense_dict.get("last_modified_date"))
    # expense.last_modified_date = to_iso_date_from_str(expense_dict.get("last_modified_date"))

    tags_data = expense_dict.get('tags', None)

    # TODO: Not sure if this belongs here or in the model class
    expense_nature = expense_nature_from_dict(expense_dict.get('nature', {}))
    expense.nature = expense_nature

    expense_category = expense_category_from_dict(expense_dict.get('category', {}))
    expense.category = expense_category

    expense_subcategory = expense_subcategory_from_dict(expense_dict.get('subcategory', {}))
    expense.subcategory = expense_subcategory

    log.info(expense.last_modified_date)

    if tags_data is not None:
        for tag_data in tags_data:
            tag = tag_from_dict(tag_data)
            if tag is not None:
                expense.add_tag(tag)
    db.session.add(expense)
    db.session.commit()
    committed_expense_dict = to_dict(expense)

    log.info(committed_expense_dict)
    _add_to_es(committed_expense_dict)
    return committed_expense_dict


def update_expense(expense_id, expense_dict):
    validate(expense_dict)
    upd_exp = Expense.query.get(expense_id)
    upd_exp.description = expense_dict.get("description", upd_exp.description)
    exp_date = expense_dict.get("expense_date")
    upd_exp.expense_date = to_date(exp_date) if exp_date else upd_exp.expense_date
    upd_exp.amount = expense_dict.get("amount", upd_exp.amount)

    tags_data = expense_dict.get('tags', None)

    # TODO: Not sure if this belongs here or in the model class

    expense_nature = expense_nature_from_dict(expense_dict.get('nature'))
    upd_exp.nature = expense_nature

    expense_category = expense_category_from_dict(expense_dict.get('category'))
    upd_exp.category = expense_category

    expense_subcategory = expense_subcategory_from_dict(expense_dict.get('subcategory'))
    upd_exp.subcategory = expense_subcategory

    upd_exp.remove_all_tags()
    if tags_data is not None:
        for tag_data in tags_data:
            tag = tag_from_dict(tag_data)
            if tag is not None:
                upd_exp.add_tag(tag)
    db.session.commit()
    committed_expense_dict = to_dict(upd_exp)
    _add_to_es(committed_expense_dict)
    return committed_expense_dict


def get_expenses(index, size):
    start_index = index if index else 0
    page_size = size if size else 50
    if start_index >= 250:
        raise ValueError("Digging too deep. Try doing a different search or lookup.")
    expenses = eq.get_expenses(datetime.datetime.now(), start_index, page_size)
    expense_dict_list = []
    for expense in expenses:
        expense_dict = to_dict(expense)
        expense_dict_list.append(expense_dict)
    return expense_dict_list


def get_expense_aggregates_for_classification(classification_type):
    if classification_type == "category":
        category_expenses_tuple_list = db.session.query(
            ExpenseCategory.name.label("category"), db.func.sum(Expense.amount).label("category_expenses")).join(
            Expense).group_by(
            ExpenseCategory.id).order_by(db.desc("category_expenses")).all()
        cat_expenses = []
        for cat_expense_tup in category_expenses_tuple_list:
            cat_expenses.append(_convert_to_json_friendly_exp_classication(cat_expense_tup, "category"))
        return cat_expenses
    elif classification_type == "subcategory":
        subcategory_expenses_tuple_list = db.session.query(
            ExpenseSubcategory.name.label("subcategory"),
            db.func.sum(Expense.amount).label("subcategory_expenses")).join(Expense).group_by(
            ExpenseSubcategory.id).order_by(db.desc("subcategory_expenses")).all()
        subcat_expenses = []
        for subcat_expense_tup in subcategory_expenses_tuple_list:
            subcat_expenses.append(_convert_to_json_friendly_exp_classication(subcat_expense_tup, "subcategory"))
        return subcat_expenses
