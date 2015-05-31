__author__ = 'srininara'

from app.queries import expense_frequency_queries as efq


def get_freq_listing():
    return efq.get_freq_listing()
