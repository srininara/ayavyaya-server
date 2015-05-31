__author__ = 'srininara'
import toolz.itertoolz as itz

from app.queries import expense_category_queries as ecq


def _make_cat_rec(cat_item):
    return {"category_id": cat_item[0][0],
            "category": cat_item[0][1],
            "cat_desc": cat_item[0][2],
            "subcategories": map(lambda val: {"subcategory_id": val[3],
                                              "subcategory": val[4], "subcategory_desc": val[5]}, cat_item[1])
            }

def get_cat_sub_cat_listing():
    raw_category_listing = ecq.get_cat_sub_cat_listing()
    cat_list_grouped_by_category = itz.groupby(lambda tup: (tup[0], tup[1], tup[2]), raw_category_listing)
    ret_val = map(_make_cat_rec, cat_list_grouped_by_category.items())
    return ret_val

    # print(cat_list_grouped_by_category)
    # ret_val = {key: map(lambda rec: rec[1], value) for (key, value) in cat_list_grouped_by_category.items()}
    # return ret_val
