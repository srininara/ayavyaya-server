#!/usr/bin/env python

__author__ = 'srininara'
import unittest
import requests


class TestFrequenciesAPI(unittest.TestCase):
    def setUp(self):
        self.frequency_list_API_url = "http://localhost:5000/grihasthi/api/v1.0/frequencies"

    def test_get_frequencies(self):
        r = requests.get(self.frequency_list_API_url)
        output = r.json()["frequencies"]
        output_len = len(output)
        self.assertTrue(output_len > 0)
        self.assertIsNotNone(output[0]["name"])
        self.assertIsNotNone(output[0]["id"])
        self.assertIsNotNone(output[0]["description"])
