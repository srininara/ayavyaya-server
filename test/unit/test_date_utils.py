from datetime import datetime
import ayavyaya.date_utils as du


def test_to_date_works():
    date_str = "2016-09-10"
    our_format = "%Y-%m-%d"
    assert date_str == datetime.strftime(du.to_date(date_str), our_format)
