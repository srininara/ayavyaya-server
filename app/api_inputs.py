from datetime import datetime
def to_date(value):
    """Parse a valid looking date in the format YYYY-mm-dd"""
    date = datetime.strptime(value, "%Y-%m-%d")
    if date.year < 1900:
        raise ValueError(u"Year must be >= 1900")
    return date

def to_str_from_datetime(value):
    dateStr = value.strftime("%Y-%m-%d")
    return dateStr
