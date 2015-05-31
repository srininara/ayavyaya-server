#!/usr/bin/env python

__author__ = 'srininara'
import unittest
import requests


class TestCategoriesAPI(unittest.TestCase):
    def setUp(self):
        self.category_list_API_url = "http://localhost:5000/grihasthi/api/v1.0/categories"

    def test_get_categories(self):
        r = requests.get(self.category_list_API_url)
        output = r.json()["categories"]
        cat_len = len(output)
        self.assertTrue(cat_len > 0)
        self.assertIsNotNone(output[0]["category"])
        self.assertIsNotNone(output[0]["category_id"])
        self.assertIsNotNone(output[0]["cat_desc"])
        self.assertIsNotNone(output[0]["subcategories"])
