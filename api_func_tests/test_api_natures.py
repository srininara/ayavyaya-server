#!/usr/bin/env python

__author__ = 'srininara'
import unittest
import requests


class TestNaturesAPI(unittest.TestCase):
    def setUp(self):
        self.nature_list_API_url = "http://localhost:5000/grihasthi/api/v1.0/natures"

    def test_get_natures(self):
        r = requests.get(self.nature_list_API_url)
        output = r.json()["natures"]
        output_len = len(output)
        self.assertTrue(output_len > 0)
        self.assertIsNotNone(output[0]["name"])
        self.assertIsNotNone(output[0]["id"])
        self.assertIsNotNone(output[0]["description"])



