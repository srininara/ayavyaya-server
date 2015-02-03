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
        output_len = len(output)
        self.assertTrue(output_len > 0)


