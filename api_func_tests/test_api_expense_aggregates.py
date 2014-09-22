#!/usr/bin/env python
import unittest
import requests
import json

class TestExpenseAggregatesAPI(unittest.TestCase):

  def setUp(self):
    self.expense_aggregates_API_url = "http://localhost:5000/grihasthi/api/v1.0/expenseAggregates/"

  def test_get_daily_expense_aggregates(self):
    input_period = "daily"
    summary = input_period + "Summary"

    # TODO: First need to check if any data is there in the db. That cannot be done now since it is not supported by the app
    r = requests.get(self.expense_aggregates_API_url + input_period)
    self.assertEqual(200, r.status_code)
    output = r.json()
    self.assertIsNotNone(output)
    self.assertIsNotNone(output[input_period])
    expenseAggregates = output[input_period]


    # At this point it is assumed that there is something in the db
    self.assertIsNotNone(expenseAggregates)
    self.assertNotEqual(len(expenseAggregates), 0)

    # TODO: Ideally we should get a bunch of expenses and find which one belongs to a single day,
    # sum it up and check the output against that
    # The above kind of setup is required for the summary piece below as well. But that will have to wait.
    self.assertIsNotNone(output[summary])
    monthExpenseAggregatesSummary = output[summary]
    print(monthExpenseAggregatesSummary)


  def test_get_daily_expense_aggregates_month_wise(self):
    input_period = "dailyMonthWise"
    summary = input_period + "Summary"
    # TODO: First need to check if any data is there in the db. That cannot be done now since it is not supported by the app
    r = requests.get(self.expense_aggregates_API_url + input_period)
    self.assertEqual(200, r.status_code)
    output = r.json()
    self.assertIsNotNone(output)
    self.assertIsNotNone(output[input_period])
    monthExpenseAggregates = output[input_period]

    # At this point it is assumed that there is something in the db
    self.assertIsNotNone(monthExpenseAggregates)

    # This is not very good way of checking stuff because it assumes things about data
    self.assertEqual(len(monthExpenseAggregates), 5)

    for monthExpenseAgg in monthExpenseAggregates:
      self.assertIsNotNone(monthExpenseAgg)
      self.assertIsNotNone(monthExpenseAgg["key"])
      self.assertIsNotNone(monthExpenseAgg["values"])

    # TODO: Ideally we should get a bunch of expenses and find which one belongs to a single day,
    # sum it up and check the output against that
    # The above kind of setup is required for the summary piece below as well. But that will have to wait.
    self.assertIsNotNone(output[summary])
    monthExpenseAggregatesSummary = output[summary]
    print(monthExpenseAggregatesSummary)



if __name__ == '__main__':
  unittest.main()
