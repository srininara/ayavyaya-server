#!/usr/bin/env python
import unittest
import requests
import json

class TestExpenseClassificationAPI(unittest.TestCase):

  def setUp(self):
    self.expense_classificaton_API_url = "http://localhost:5000/grihasthi/api/v1.0/expenseClassification/"


  def test_get_category_expense_classification(self):
    input_classification = "category"
    # TODO: First need to check if any data is there in the db. That cannot be done now since it is not supported by the app
    r = requests.get(self.expense_classificaton_API_url + input_classification)
    self.assertEqual(200, r.status_code)
    output = r.json()
    print(output)
    self.assertIsNotNone(output)
    self.assertIsNotNone(output[input_classification])
    expenseClassification = output[input_classification]


    # At this point it is assumed that there is something in the db
    self.assertIsNotNone(expenseClassification)
    self.assertNotEqual(len(expenseClassification), 0)

    # TODO: Ideally we should get a bunch of expenses and find which one belongs to a single category,
    # sum it up and check the output against that

  def test_get_subcategory_expense_classification(self):
    input_classification = "subcategory"
    # TODO: First need to check if any data is there in the db. That cannot be done now since it is not supported by the app
    r = requests.get(self.expense_classificaton_API_url + input_classification)
    self.assertEqual(200, r.status_code)
    output = r.json()
    print(output)
    self.assertIsNotNone(output)
    self.assertIsNotNone(output[input_classification])
    expenseClassification = output[input_classification]


    # At this point it is assumed that there is something in the db
    self.assertIsNotNone(expenseClassification)
    self.assertNotEqual(len(expenseClassification), 0)

    print(expenseClassification)
    # TODO: Ideally we should get a bunch of expenses and find which one belongs to a single category,
    # sum it up and check the output against that


if __name__ == '__main__':
  unittest.main()
