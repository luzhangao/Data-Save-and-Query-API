# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description: test store API
"""

import unittest
import ast
import requests
from tests.correct_results import insert_cases


class TestStoreAPI(unittest.TestCase):
    def setUp(self):
        """
        set up the request session
        :return: None
        """
        self.hello_url = "http://localhost:7000"
        self.store_url = self.hello_url + "/store"
        self.session = requests.session()

    def tearDown(self):
        """

        :return: None
        """
        pass

    def test_hello_world(self):
        """
        test hello world
        :return: None
        """
        response = self.session.get(self.hello_url)
        self.assertEqual(response.json(), {'current_version': 'V1.0.0'})

    def test_insert_data(self):
        """
        test insert data
        :return: None
        """
        # test all cases
        for case in insert_cases:
            response = self.session.post(self.store_url, ast.literal_eval(case))
            self.assertEqual(response.json(), insert_cases[case])


if __name__ == '__main__':
    pass
