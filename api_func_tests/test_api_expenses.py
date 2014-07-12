#!/usr/bin/env python
import unittest
import requests
import json

class TestExpensesAPI(unittest.TestCase):

  def setUp(self):
    self.expense_list_API_url = "http://localhost:5000/grihasthi/api/v1.0/expenses"

  def test_postExpenses(self):
    payload = {'description':'ssssttt', 'expense_date':'2014-06-29', 'amount':'110.10'}
    headers = {'content-type': 'application/json'}

    r = requests.post(self.expense_list_API_url,data=json.dumps(payload),headers=headers)
    self.assertEqual(201,r.status_code)
    output = json.loads(r.json())
    print(output['id'])
    self.assertTrue(output.get('id',-1)!=-1)

  # def test_postExpenses_without_description(self):
  #   payload = {'expense_date':'2014-06-29', 'amount':'120.10'}
  #   headers = {'content-type': 'application/json'}
  #
  #   r = requests.post(self.expense_list_API_url,data=json.dumps(payload),headers=headers)
  #   self.assertEqual(400,r.status_code)

if __name__ == '__main__':
  unittest.main()
