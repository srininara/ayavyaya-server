__author__ = 'srininara'

from ayavyaya.queries import expense_nature_queries as enq


def get_nat_listing():
    return enq.get_nat_listing()
