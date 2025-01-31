from datetime import datetime

from dateutil.relativedelta import *


def to_date(value):
    date = datetime.strptime(value, "%Y-%m-%d")
    if date.year < 1900:
        raise ValueError(u"Year must be >= 1900")
    return date


def to_str_from_datetime(value):
    datestr = value.strftime("%Y-%m-%d")
    return datestr


def to_iso_str_from_datetime(value):
    datestr = value.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return datestr


def to_iso_date_from_str(value):
    date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    return date


def calc_month_key(some_date):
    return some_date.strftime("%m") + ":" + some_date.strftime("%B") + ":" + some_date.strftime("%Y")


def to_first_day_from_mth_str(value):
    return datetime.strptime(value, "%Y-%m")


def add_a_month_to(the_date):
    return the_date + relativedelta(months=+1)


def prev_month_to(the_date):
    return the_date + relativedelta(months=-1)
