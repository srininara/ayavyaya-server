#!/usr/bin/env python
import unittest
import requests
import json
from random import randint
from datetime import datetime


class TestExpensesAPI(unittest.TestCase):
    def setUp(self):
        self.expense_list_API_url = "http://localhost:5000/grihasthi/api/v1.0/expenses"

    def _test_post_expenses_without_tags(self):
        payload = {'description': 'test expense without tag'
            , 'expense_date': '2014-07-31', 'amount': '110.10', 'category': 'Apparel'
            , 'subcategory': 'Regular Wear', 'nature': 'Necessity', 'frequency': 'Regular'}
        headers = {'content-type': 'application/json'}

        r = requests.post(self.expense_list_API_url, data=json.dumps(payload), headers=headers)
        self.assertEqual(201, r.status_code)
        output = r.json()

        self.assertTrue(output.get('id', -1) != -1)
        self.assertEqual(output.get('nature', ""), 'Necessity')
        self.assertTrue(output.get('nature_id', -1) != -1)
        self.assertEqual(output.get('category', ""), 'Apparel')
        self.assertTrue(output.get('category_id', -1) != -1)
        self.assertEqual(output.get('subcategory', ""), 'Regular Wear')
        self.assertTrue(output.get('subcategory_id', -1) != -1)
        self.assertEqual(output.get('frequency', ""), 'Regular')
        self.assertTrue(output.get('frequency_id', -1) != -1)

        tags = output.get('tags')
        self.assertIsNotNone(tags)
        self.assertEqual(len(tags), 0)

    # def test_post_expenses_with_non_existant_category(self):

    def _test_post_expenses_with_tags(self):
        payload = {'description': 'test expense with tag', 'expense_date': '2015-02-02'
            , 'amount': '110.10', 'tags': [{"name": "testTag1"}, {"name": "testTag2"}]
            , 'category': 'Apparel', 'subcategory': 'Regular Wear', 'nature': 'Necessity'
            , 'frequency': 'Regular'}
        headers = {'content-type': 'application/json'}

        r = requests.post(self.expense_list_API_url, data=json.dumps(payload), headers=headers)
        self.assertEqual(201, r.status_code)
        output = r.json()
        self.assertTrue(output.get('id', -1) != -1)
        self.assertTrue(output.get('nature_id', -1) != -1)
        self.assertTrue(output.get('category_id', -1) != -1)
        self.assertTrue(output.get('subcategory_id', -1) != -1)
        self.assertTrue(output.get('frequency_id', -1) != -1)

        tags = output.get('tags')
        self.assertIsNotNone(tags)
        self.assertEqual(len(tags), 2)


    def test_get_expenses_default(self):
        r = requests.get(self.expense_list_API_url)
        output = r.json()["expenses"]
        output_len = len(output)
        self.assertTrue(output_len <= 20)
        rand_index = randint(0, output_len)
        test_rec = output[rand_index]
        test_date = datetime.strptime(test_rec["expense_date"], "%Y-%m-%d")
        self.assertTrue(test_date <= datetime.now())



        # def test_postExpenses_without_description(self):
        # payload = {'expense_date':'2014-06-29', 'amount':'120.10'}
        #   headers = {'content-type': 'application/json'}
        #
        #   r = requests.post(self.expense_list_API_url,data=json.dumps(payload),headers=headers)
        #   self.assertEqual(400,r.status_code)



if __name__ == '__main__':
    unittest.main()
