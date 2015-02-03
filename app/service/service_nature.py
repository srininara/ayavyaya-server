__author__ = 'srininara'

from app.queries import expense_nature_queries as enq


def get_nat_listing():
    return map(lambda x: x[0], enq.get_nat_listing())
