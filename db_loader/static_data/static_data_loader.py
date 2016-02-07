#!/usr/bin/env python
import csv
import os

from sqlalchemy import create_engine, MetaData



# SQLALCHEMY_DATABASE_URI = 'postgresql://grihasthi_app:grihasthi_app1!@localhost/grihasthi_db'
# SQLALCHEMY_DATABASE_URI = 'postgresql://ayavyaya_app:ayavyaya_app1@localhost/ayavyaya_db'


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    '../../',
    'expense.db')

engine = create_engine(SQLALCHEMY_DATABASE_URI)
# meta = MetaData(bind=engine)
# expense_nature = Table('expense_nature', meta, autoload=True, autoload_with=engine)

meta = MetaData()
meta.reflect(bind=engine)
expense_nature = meta.tables['expense_nature']
expense_frequency = meta.tables['expense_frequency']
expense_category = meta.tables['expense_category']
expense_subcategory = meta.tables['expense_subcategory']
connection = engine.connect()
NOT_AVAILABLE_NAME = "Not Available"
NOT_AVAILABLE_DESC = "Data Not Available"
NO_SUBCATEGORY = "No Subcategory"
NOT_AVAILABLE_ID = -1000

with open('expense_nature.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    count = 0
    for row in reader:
        name = row['name']
        description = row['description']
        ins = expense_nature.insert(values=dict(name=name, description=description))
        result = connection.execute(ins)
    na_ins = expense_nature.insert(values=dict(id=NOT_AVAILABLE_ID, name=NOT_AVAILABLE_NAME,
                                               description=NOT_AVAILABLE_DESC))
    na_result = connection.execute(na_ins)

with open('expense_frequency.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    count = 0
    for row in reader:
        name = row['name']
        description = row['description']
        ins = expense_frequency.insert(values=dict(name=name, description=description))
        result = connection.execute(ins)
    na_ins = expense_frequency.insert(values=dict(id=NOT_AVAILABLE_ID, name=NOT_AVAILABLE_NAME,
                                                  description=NOT_AVAILABLE_DESC))
    na_result = connection.execute(na_ins)

categories = {}

with open('expense_category.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    count = 0
    for row in reader:
        name = row['name']
        description = row['description']
        ins = expense_category.insert(values=dict(name=name, description=description))
        result = connection.execute(ins)
        categories[name] = result.inserted_primary_key[0]

    na_ins = expense_category.insert(values=dict(id=NOT_AVAILABLE_ID, name=NOT_AVAILABLE_NAME,
                                                  description=NOT_AVAILABLE_DESC))
    na_result = connection.execute(na_ins)

with open('expense_subcategory.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    count = 0
    for row in reader:
        name = row['name']
        description = row['description']
        category_id = categories[row['category']]
        ins = expense_subcategory.insert(values=dict(name=name, description=description, category_id=category_id))
        result = connection.execute(ins)

    na_ins = expense_subcategory.insert(values=dict(id=NOT_AVAILABLE_ID, name=NOT_AVAILABLE_NAME,
                                                  description=NOT_AVAILABLE_DESC, category_id=NOT_AVAILABLE_ID))
    na_result = connection.execute(na_ins)

    for category, category_id in categories.iteritems():
        in_cat_na_ins = expense_subcategory.insert(values=dict(id=-1*category_id, name=category+"-"+NO_SUBCATEGORY,
                                                  description=NOT_AVAILABLE_DESC, category_id=category_id))
        in_cat_na_result = connection.execute(in_cat_na_ins)

connection.close()
