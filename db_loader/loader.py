#!/usr/bin/env python
import csv
import requests
import json
import logging
from datetime import datetime

# Slno,Date,Description,Amount,Tag1,Tag2
expense_list_API_url = "http://localhost:5000/grihasthi/api/v1.0/expenses"

logging.basicConfig(level=logging.INFO)


def convert(value):
    return (datetime.strptime(value, "%d-%b-%Y")).strftime("%Y-%m-%d")


def post_expenses(date, description, amount, category, subcategory, nature, frequency, tag1, tag2):
    payload = {'description': description,
               'expense_date': date, 'amount': amount, 'category': category,
               'nature': nature, 'frequency': frequency
               }
    if subcategory:
        # print(subcategory.split(":")[1])
        payload['subcategory'] = subcategory.split(":")[1]

    if tag1:
        tags = [{"name": tag1}]
        if tag2:
            tags.append({"name": tag2})
        payload['tags'] = tags

    headers = {'content-type': 'application/json'}

    r = requests.post(expense_list_API_url, data=json.dumps(payload), headers=headers)
    if 201 != r.status_code:
        raise RuntimeError("insert failed")


with open('DailyExpenseTrackerV2.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    count = 0
    for row in reader:
        if row['Date'] == "":
            break
        count+=1
        if count%100 == 0:
            logging.info("Inserted records: " + str(count)); 
            
        post_expenses(convert(row['Date']), row['Description'], row['Amount'], row['Category']
                      , row['Sub Category'], row['Nature'], row['Frequency'], row['Tag1'], row['Tag2'])

    logging.info("Total inserted records: " + str(count));
    