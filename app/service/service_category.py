__author__ = 'srininara'
import toolz.itertoolz as itz

from app.queries import expense_category_queries as ecq


def get_cat_sub_cat_listing():
    raw_category_listing = ecq.get_cat_sub_cat_listing()
    cat_list_grouped_by_category = itz.groupby(lambda tup: tup[0], raw_category_listing)
    ret_val = {key: map(lambda rec: rec[1], value) for (key, value) in cat_list_grouped_by_category.items()}
    return ret_val

