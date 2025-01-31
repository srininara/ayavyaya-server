#!/usr/bin/env python
import unittest
import json
from random import randint
from datetime import datetime

import requests


NOT_AVAILABLE_NAME = "Not Available"

class TestExpensesAPI(unittest.TestCase):
    def setUp(self):
        self.expense_list_API_url = "http://localhost:5000/grihasthi/api/v1.0/expenses"
        self.headers = {'content-type': 'application/json'}

    def _create_expense_without_tags(self):
        category = dict(name='Apparel')
        subCategory = dict(name="Regular Wear")
        nature = dict(name="Necessity")
        return dict(description='test expense without tag', expense_date='2016-03-12', amount='110.10',
                    category=category, subcategory=subCategory, nature=nature, last_modified_date=datetime.now().isoformat())

    def _create_expense_with_tags(self):
        expense = self._create_expense_without_tags()
        expense['description']='test expense with tag'
        expense['tags']=[{"name": "testTag1"}, {"name": "testTag2"}]
        return expense
        # category = dict(name='Apparel')
        # subCategory = dict(name="Regular Wear")
        # nature = dict(name="Necessity")
        # return dict(description='test expense with tag', expense_date='2015-03-15', amount='110.10',
        #             tags=[{"name": "testTag1"}, {"name": "testTag2"}], category=category, subcategory=subCategory, nature=nature)

    def test_post_expenses_without_tags(self):
        payload = self._create_expense_without_tags()

        r = requests.post(self.expense_list_API_url, data=json.dumps(payload), headers=self.headers)
        self.assertEqual(201, r.status_code)
        output = r.json()

        self.assertTrue(output.get('id', -1) != -1)
        output_nature = output.get('nature', {})
        output_category = output.get('category', {})
        output_subcategory = output.get('subcategory', {})

        self.assertEqual(output_nature.get('name', ""), 'Necessity')
        self.assertTrue(output_nature.get('id', -1) != -1)
        self.assertEqual(output_category.get('name', ""), 'Apparel')
        self.assertTrue(output_category.get('id', -1) != -1)
        self.assertEqual(output_subcategory.get('name', ""), 'Regular Wear')
        self.assertTrue(output_subcategory.get('id', -1) != -1)

        self.assertIsNotNone(output.get('last_modified_date'))
        self.assertEqual(payload.get("last_modified_date"),output.get('last_modified_date'))

        tags = output.get('tags')
        self.assertIsNotNone(tags)
        self.assertEqual(len(tags), 0)

    # def test_post_expenses_with_non_existent_category(self):

    def _test_post_expenses_with_tags(self):
        payload = self._create_expense_with_tags()
        headers = {'content-type': 'application/json'}

        r = requests.post(self.expense_list_API_url, data=json.dumps(payload), headers=headers)
        self.assertEqual(201, r.status_code)
        output = r.json()
        output_nature = output.get('nature', {})
        output_category = output.get('category', {})
        output_subcategory = output.get('subcategory', {})

        self.assertTrue(output.get('id', -1) != -1)
        self.assertTrue(output_nature.get('id', -1) != -1)
        self.assertTrue(output_category.get('id', -1) != -1)
        self.assertTrue(output_subcategory.get('id', -1) != -1)

        tags = output.get('tags')
        self.assertIsNotNone(tags)
        self.assertEqual(len(tags), 2)

    def _test_get_expenses_default(self):
        r = requests.get(self.expense_list_API_url)
        output = r.json()["expenses"]
        output_len = len(output)
        self.assertTrue(output_len <= 50)
        rand_index = randint(0, output_len)
        test_rec = output[rand_index]
        test_date = datetime.strptime(test_rec["expense_date"], "%Y-%m-%d")
        self.assertTrue(test_date <= datetime.now())
        self.assertGreater(test_rec["amount"],0, "Amount must be greater than 0")
        self.assertTrue(test_rec["category"]["name"])
        self.assertTrue(test_rec["subcategory"]["name"])
        self.assertTrue(test_rec["nature"]["name"])
        self.assertTrue(test_rec["description"] or test_rec["category"])

    def _test_get_expenses_with_pagination_parameters(self):
        paginated_url = self.expense_list_API_url + "?index=0&size=2"
        r = requests.get(paginated_url)
        first_output = r.json()["expenses"]
        first_output_len = len(first_output)
        self.assertTrue(first_output_len == 2)

        paginated_url = self.expense_list_API_url + "?index=1&size=5"
        r = requests.get(paginated_url)
        second_output = r.json()["expenses"]
        second_output_len = len(second_output)
        self.assertTrue(second_output_len == 5)

        self.assertTrue(first_output[1]["id"] == second_output[0]["id"])


    def _test_get_expenses_fails_when_pagination_index_is_equal_or_greater_than_250(self):
        paginated_url = self.expense_list_API_url + "?index=250&size=2"
        r = requests.get(paginated_url)
        self.assertTrue(r.status_code==400)
        paginated_url = self.expense_list_API_url + "?index=251&size=2"
        r = requests.get(paginated_url)
        self.assertTrue(r.status_code==400)
        paginated_url = self.expense_list_API_url + "?index=249&size=2"
        r = requests.get(paginated_url)
        self.assertTrue(r.status_code==200)



    def _test_update_expenses(self):
        r = requests.get(self.expense_list_API_url)
        records = r.json()["expenses"]
        print(records)
        output_len = len(records)
        rand_index = randint(0, output_len-1)
        update_rec = records[rand_index]
        updated_desc = update_rec.get("description") + " updated"
        update_rec["description"] = updated_desc

        up_r = requests.put(self.expense_list_API_url + "/" + str(update_rec.get("id")), data=json.dumps(update_rec),
                            headers=self.headers)

        self.assertEqual(200, up_r.status_code)
        # TODO: Getting all the expenses in the world is not the best idea
        r_u = requests.get(self.expense_list_API_url)
        records_u = r_u.json()["expenses"]
        for rec in records_u:
            if rec.get("id") == update_rec.get("id"):
                self.assertEqual(rec.get("description"), update_rec.get("description"))

    # This is not what we want for the future. We want at least description or category
    def _test_postExpenses_with_only_date_and_amount_is_allowed(self):
        payload = {'expense_date': '2015-07-01', 'amount': '120.10'}

        r = requests.post(self.expense_list_API_url, data=json.dumps(payload), headers=self.headers)
        self.assertEqual(201, r.status_code)
        created_expense = r.json()
        print(created_expense)
        self.assertIsNotNone(created_expense)
        self.assertIsNotNone(created_expense.get("id"))
        self.assertIsNotNone(created_expense.get("nature"))
        self.assertIsNotNone(created_expense.get("category"))
        self.assertIsNotNone(created_expense.get("subcategory"))

    def _test_create_a_normal_expense_without_tags_and_then_update_it_to_have_only_date_and_amount(self):
        payload = self._create_expense_without_tags()

        r = requests.post(self.expense_list_API_url, data=json.dumps(payload), headers=self.headers)
        self.assertEqual(201, r.status_code)
        output = r.json()

        self.assertTrue(output.get('id', -1) != -1)

        payload = {'id': output.get('id'),'expense_date': '2015-07-01', 'amount': '120.10'}
        up_r = requests.put(self.expense_list_API_url + "/" + str(output.get("id")), data=json.dumps(payload),
                            headers=self.headers)

        self.assertEqual(200, up_r.status_code)
        up_rec = up_r.json()
        self.assertEqual(output.get("id"),up_rec.get("id"))
        # More assertsadded for checking whether the values of category etc. have got updated to Not Available.
        self.assertEqual(up_rec.get("nature"), NOT_AVAILABLE_NAME)
        self.assertEqual(up_rec.get("category"), NOT_AVAILABLE_NAME)
        self.assertEqual(up_rec.get("subcategory"), NOT_AVAILABLE_NAME)
        self.assertTrue(up_rec.get("nature_id") < 0)
        self.assertTrue(up_rec.get("category_id") < 0)
        self.assertTrue(up_rec.get("subcategory_id") < 0)





if __name__ == '__main__':
    unittest.main()
