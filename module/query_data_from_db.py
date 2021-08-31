# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description: Query the data from mongodb
"""

from utils.mongodb_util import db_test
from config.config import DB_test


class Query(object):
    def __init__(self):
        self.db_connection = db_test(DB_test)

    @staticmethod
    def op_equal(prop, value):
        """
        Operator EQUAL
        :param prop: string
               e.g. "id", "views"
        :param value: string or int
               e.g. "first-post", 100
        :return: dict
        """
        return {prop: value}

    @staticmethod
    def op_greater_than(prop, value):
        """
        Operator GREATER_THAN
        :param prop: string
               e.g. "views"
        :param value: int
               e.g. 100
        :return: dict
        """
        return {prop: {"$gt": value}}

    @staticmethod
    def op_less_than(prop, value):
        """
        Operator LESS_THAN
        :param prop: string
               e.g. "views"
        :param value: int
               e.g. 100
        :return: dict
        """
        return {prop: {"$lt": value}}

    @staticmethod
    def op_and(op_a, op_b):
        """
        Operator AND
        :param op_a: dict
               e.g. self.op_equal(x, xx)
        :param op_b: dict
               e.g. self.op_equal(x, xx)
        :return: dict
        """
        return {"$and": [op_a, op_b]}

    @staticmethod
    def op_or(op_a, op_b):
        """
        Operator OR
        :param op_a: dict
               e.g. self.op_equal(x, xx)
        :param op_b: dict
               e.g. self.op_equal(x, xx)
        :return: dict
        """
        return {"$or": [op_a, op_b]}

    def op_not(self, op_a):
        """
        Operator NOT
        There are some cases:
        {'views': {'$gt': 100}}  -> {'views': {'$not': {'$gt': 100}}}
        {'views': 100}  -> {'views': {'$ne': 100}}
        {'$and': [{'id': 'first-post'}, {'views': 100}]} -> {'$or': [{'id': {'$ne': 'first-post'}}, {'views': {'$ne': 100}}]}
        {'$and': [{'id': 'first-post'}, {'views': {'$gt': 100}}]} -> {'$or': [{'id': {'$ne': 'first-post'}}, {'views': {'$not': {'gt': 100}}}]}
        {'$or': [{'id': 'first-post'}, {'views': {'$gt': 100}}]} -> {'$and': [{'id': {'$ne': 'first-post'}}, {'views': {'$not': {'gt': 100}}}]}
        :param op_a: dict
               e.g. self.op_equal(x, xx)
        :return: dict
        """
        condition = dict()
        """
        Key points:
        1. use "$not" for "greater or less than XXX"
        2. use "$ne" for "equal to XXX"
        """
        for key in op_a:
            # {'views': {'$gt': 100}}  -> {'views': {'$not': {'$gt': 100}}}
            if isinstance(op_a[key], dict):
                condition[key] = {"$not": op_a[key]}
            # {'$and': [{'id': 'first-post'}, {'views': {'$gt': 100}}]} ->
            # {'$or': [{'id': {'$ne': 'first-post'}}, {'views': {'$not': {'gt': 100}}}]}
            elif isinstance(op_a[key], list):
                temp_values = list()
                for elem in op_a[key]:  # {'id': 'first-post'}, {'views': {'$gt': 100}}
                    temp_values.append(self.op_not(elem))
                # ATTENTION: exchange $and and $or (De Morgan's laws)
                if key == "$and":
                    condition["$or"] = temp_values
                elif key == "$or":
                    condition["$and"] = temp_values
            # {'views': 100}  -> {'views': {'$ne': 100}}
            else:
                condition[key] = {"$ne": op_a[key]}
        return condition

    # TODO Mongodb can not identify nested and/or sentences
    def execute_query(self, query_condition):
        """
        execute the query
        :param query_condition: dict
               e.g. {"view": {"$gt": 100}}
        :return: a cursor from mongodb
        """
        # query_condition = self.cancellation(query_condition)
        return self.db_connection.find(query_condition, {"_id": 0})  # remove "_id"


if __name__ == '__main__':
    q = Query()
    print(q.op_equal("views", 100))
    print(q.op_greater_than("views", 100))
    print(q.op_less_than("views", 100))

    print(list(q.execute_query({"$and": [{'views': {'$gt': 100}}, {"id": "fourth-post"}]})))
    print(list(q.execute_query({"$or": [{'views': {'$lt': 10}}, {"$and": [{'views': {'$gt': 100}}, {"id": "fourth-post"}]}]})))
    print(list(q.execute_query({'views': {"$not": {'$lt': 500}}})))
    print(list(q.execute_query({'views': {"$ne": 100}})))
    print(list(q.execute_query(q.op_not(q.op_equal("id", "fourth-post")))))
    print(list(q.execute_query(q.op_or(q.op_equal("id", "fourth-post"), q.op_greater_than("views", 200)))))
    print(list(q.execute_query(
        q.op_or(
            q.op_and(q.op_equal("id", "fourth-post"), q.op_greater_than("views", 200)),
            q.op_not(q.op_equal("views", 100))))))

    print(list(q.execute_query({'$and': [{'id': {'$ne': 'first-post'}}, {'views': {'$ne': 100}}]})))
    print(list(q.execute_query({'$and': [{'id': {'$ne': 'third-post'}}, {'views': {'$not': {'$gt': 100}}}]})))

