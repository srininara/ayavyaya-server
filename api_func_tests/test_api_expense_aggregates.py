#!/usr/bin/env python
import unittest
import requests
import json

class TestExpenseAggregatesAPI(unittest.TestCase):

  def setUp(self):
    self.expense_aggregates_API_url = "http://localhost:5000/grihasthi/api/v1.0/expenseAggregates/"

#   def test_get_daily_expense_aggregates(self):
#     input_period = "daily"
#     # TODO: First need to check if any data is there in the db. That cannot be done now since it is not supported by the app
#     r = requests.get(self.expense_aggregates_API_url + input_period)
#     self.assertEqual(200, r.status_code)
#     output = r.json()
#     print(output)
#     self.assertIsNotNone(output)
#     self.assertIsNotNone(output[input_period])
#     expenseAggregates = output[input_period]
#
#
#     # At this point it is assumed that there is something in the db
#     self.assertIsNotNone(expenseAggregates)
#     self.assertNotEqual(len(expenseAggregates), 0)
#
#     # print(expenseAggregates)
#     # TODO: Ideally we should get a bunch of expenses and find which one belongs to a single day,
#     # sum it up and check the output against that


  def test_get_daily_expense_aggregates_month_wise(self):
    input_period = "dailyMonthWise"
    # TODO: First need to check if any data is there in the db. That cannot be done now since it is not supported by the app
    r = requests.get(self.expense_aggregates_API_url + input_period)
    self.assertEqual(200, r.status_code)
    output = r.json()
#     print(output)
    self.assertIsNotNone(output)
    self.assertIsNotNone(output[input_period])
    monthExpenseAggregates = output[input_period]
    # print(monthExpenseAggregates)

    # At this point it is assumed that there is something in the db
    self.assertIsNotNone(monthExpenseAggregates)

    # This is not very good way of checking stuff because it assumes things about data
    self.assertEqual(len(monthExpenseAggregates), 4)

    for monthExpenseAgg in monthExpenseAggregates:
      self.assertIsNotNone(monthExpenseAgg)
      self.assertIsNotNone(monthExpenseAgg["key"])
      self.assertIsNotNone(monthExpenseAgg["values"])



    # print(expenseAggregates)
    # TODO: Ideally we should get a bunch of expenses and find which one belongs to a single day,
    # sum it up and check the output against that


if __name__ == '__main__':
  unittest.main()
