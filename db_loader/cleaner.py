#!/usr/bin/env python
import csv
import os
import logging

from sqlalchemy import create_engine, MetaData, select, func



# SQLALCHEMY_DATABASE_URI = 'postgresql://grihasthi_app:grihasthi_app1!@localhost/grihasthi_db'
# SQLALCHEMY_DATABASE_URI = 'postgresql://ayavyaya_app:ayavyaya_app1@localhost/ayavyaya_db'


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    '../',
    'expense.db')
logging.basicConfig(level=logging.INFO)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

meta = MetaData()
meta.reflect(bind=engine)
expenses_tags = meta.tables['expenses_tags']
tag = meta.tables['tag']
expense = meta.tables['expense']
connection = engine.connect()
count_expenses = connection.execute(select([func.count()]).select_from(expense)).scalar()
logging.info("Going to delete expenses. Count is " + str(count_expenses)); 
del_e_t = expenses_tags.delete()
connection.execute(del_e_t)
del_t = tag.delete()
connection.execute(del_t)
del_e = expense.delete()
connection.execute(del_e)
connection.close()
