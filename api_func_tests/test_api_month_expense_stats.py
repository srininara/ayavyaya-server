__author__ = 'srininara'
import unittest
import requests
import json

class TestMonthlyExpenseStatsAPI(unittest.TestCase):

  def setUp(self):
    self.monthly_expense_stats_API_url = "http://localhost:5000/grihasthi/api/v1.0/monthStatsCategory/"

  def test_get_daily_expense_aggregates(self):
    input_month = "2015-7"


    r = requests.get(self.monthly_expense_stats_API_url + input_month)
    self.assertEqual(200, r.status_code)
    output = r.json()
    print(output)

if __name__ == '__main__':
  unittest.main()

