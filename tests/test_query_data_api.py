# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/25
@description: test query API
"""

import unittest
import ast
import requests

from config.config import DB_test, sample_cases
from tests.correct_results import query_cases
from utils.mongodb_util import db_test


class TestStoreAPI(unittest.TestCase):
    def setUp(self):
        """
        set up the request session and insert cases into database
        :return:
        """
        self.hello_url = "http://localhost:7000"
        self.store_url = self.hello_url + "/store"
        self.session = requests.session()

        self.db_connection = db_test(DB_test)
        for case in sample_cases:
            self.db_connection.insert_one(sample_cases[case])

    def tearDown(self):
        """
        remove all test cases from database
        :return: None
        """
        for case in sample_cases:
            self.db_connection.delete_one(sample_cases[case])

    def test_hello_world(self):
        """
        test hello world
        :return: None
        """
        response = self.session.get(self.hello_url)
        self.assertEqual(response.json(), {'current_version': 'V1.0.0'})

    def test_query(self):
        """
        test query cases
        :return: None
        """
        for case in query_cases:
            params = ast.literal_eval(case)
            response = self.session.get(self.store_url, params=params)
            self.assertEqual(response.json(), query_cases[case])


if __name__ == '__main__':
    pass
