# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description: parse query strings
EQUAL(property, value) <=> entity.property = value
AND(sub_operator_a, sub_operator_b) <=> both sub_operator_a and sub_operator_b are true
OR(sub_operator_a, sub_operator_b) <=> either sub_operator_a and sub_operator_b is true or both true
NOT(sub_operator_a) <=> sub_operator_a is false
GREATER_THAN(property, value) <=> entity.property > value, valid only for number values
LESS_THAN(property, value) <=> entity.property < value, valid only for number values
"""

import re
import traceback
import ast
from module.query_data_from_db import Query
from config.config import sample_cases
from utils.log import LOG


class ParseQuery(Query):
    def __init__(self):
        super().__init__()
        self.is_error = False

    def get_para(self, query):
        """
        get property and value from string if the operation is in ["EQUAL", "GREATER_THAN", "LESS_THAN"]
        ("id","first-post") -> ("id", "first-post")
        :param query: string
        :return: (prop, value)
        """
        m = re.match(r"\((.*?)\,(.*?)\)", query)
        if not self.check_regex_error(m, query, 2):
            prop = ast.literal_eval(m.groups()[0])  # "id" -> id
            value = ast.literal_eval(m.groups()[1])  # 100 (string) -> 100 (int), "first" -> first
        else:
            prop = ""
            value = ""
        return prop, value

    @staticmethod
    def parentheses_counter(query):
        """
        find the index of the string when the number of left parentheses equals the number of right parentheses
        NOT(OR(EQUAL("id","third-post"),GREATER_THAN("views",100))),OR(EQUAL("id","third-post"),EQUAL("id","fourth-post"))
        ->
        NOT(OR(EQUAL("id","third-post"),GREATER_THAN("views",100)))
        OR(EQUAL("id","third-post"),EQUAL("id","fourth-post"))
        :param query: string
        :return: int
        """
        left = 0
        right = 0
        for ind in range(len(query)):
            single = query[ind]
            if single == "(":
                left += 1
            elif single == ")":
                right += 1
            if left == right and left != 0:
                return ind
        return 0

    def get_sub_operation(self, query, operation="NOT"):
        """
        get sub operations from the string if the operation is in ["NOT", "AND", "OR"]
        if main operation is "NOT", return op_a
        else return (op_a, op_b)
        :param query: string
        :param operation: string
               the main operation, "NOT", "AND", "OR"
        :return: (op_a, op_b) or op_a
        """
        # print(query, operation)
        if operation == "NOT":
            # There are one operation in NOT: operation().
            m = re.match(r"^\((.*)\)$", query)
            if not self.check_regex_error(m, query):  # If no error
                op_a = m.groups()[0]
                return op_a
            else:
                return ""
        else:
            # There are two individual operations in AND/OR. Each operation must have a pattern: operation(), and is
            # connected with ","
            m = re.match(r"^\((.+)\)$", query)
            if not self.check_regex_error(m, query, 1):  # If no error
                need_split = m.groups()[0]
                ind = self.parentheses_counter(need_split)  # ind is the index of the last ")"
                op_a = need_split[: ind+1]  # So use ind + 1 to cover the last ")"
                op_b = need_split[ind+2:]  # Use ind + 2 to remove the ","
                return op_a, op_b
            else:
                return ""

    def check_regex_error(self, m, query, group_numbers=1):
        """
        check if there is no groups or not enough groups in re.match
        :param m: re.match
        :param query: string
               used to print logs
        :param group_numbers: int
               The number of groups
        :return: boolean
                True = There are some errors
                False = No errors
        """
        if m and group_numbers == 1:  # If m has groups
            return False
        if m and group_numbers >= 1:  # If m has more than one group
            if len(m.groups()) == group_numbers:  # Then check the group numbers
                return False
            else:
                self.is_error = True
                LOG.error("Parse query error! Query string is %s" % query)
                return True
        else:
            self.is_error = True
            LOG.error("Parse query error! Query string is %s" % query)
            return True

    def check_value_type(self, value, *args):
        """
        check the type of values, e.g. the value for GREATER_THEN can not be string
        :param value: string/int/float/boolean
        :return: boolean
                True => correct
                Flase => something is wrong
        """
        if type(value) in args:
            return True
        else:
            self.is_error = True
            LOG.error("Value type error! Value is %s, and the current value type is %s" % (str(value), type(value)))

    @staticmethod
    def pre_process_string(query):
        """
        pre process the string
        1. remove all blanks
        2. EQUAL(id,"abc") -> EQUAL("id","abc")
        :param query: string
        :return: string
        """
        query = query.replace(" ", "")
        for case_name in sample_cases:
            for key in sample_cases[case_name]:
                if "\"" + key + "\"" not in query and "\'" + key + "\'" not in query:  # "id" or 'id' not in query
                    query = query.replace(key, "\"" + key + "\"")  # id -> "id"
        return query

    def parse_query_string(self, query):
        """
        parse the query
        :param query: string
        :return: dict or ""
                e.g. {'id': 'first-post'}, {'$and': [{'id': {'$ne': 'first-post'}}, {'views': 100}]}
        """
        m = re.match(r"(.+?)\(", query)  # EQUAL("id","first-post") -> (EQUAL,)
        # print(m.groups(), query)
        if not self.check_regex_error(m, query):
            op = m.groups()[0]
            # query[len(op):] => EQUAL("id","first-post") -> ("id","first-post")
            if op == "EQUAL":
                prop, value = self.get_para(query[len(op):])
                return self.op_equal(prop, value)
            elif op == "GREATER_THAN":
                prop, value = self.get_para(query[len(op):])
                self.check_value_type(value, int, float)
                return self.op_greater_than(prop, value)
            elif op == "LESS_THAN":
                prop, value = self.get_para(query[len(op):])
                self.check_value_type(value, int, float)
                return self.op_less_than(prop, value)
            elif op == "AND":
                op_a, op_b = self.get_sub_operation(query[len(op):], operation="AND")
                final_a, final_b = self.parse_query_string(op_a), self.parse_query_string(op_b)
                return self.op_and(final_a, final_b)
            elif op == "OR":
                op_a, op_b = self.get_sub_operation(query[len(op):], operation="OR")
                final_a, final_b = self.parse_query_string(op_a), self.parse_query_string(op_b)
                return self.op_or(final_a, final_b)
            elif op == "NOT":
                op_a = self.get_sub_operation(query[len(op):], operation="NOT")
                final_a = self.parse_query_string(op_a)
                return self.op_not(final_a)
            else:
                self.is_error = True
                LOG.error("Parse query error! Query string is %s" % query)
                return ""
        else:
            return ""


def parse_query_string_bak(query):
    """
    This method is cool but not recommended for use. It is not safe.
    EQUAL(id,"abc") ->  q.op_equal("id","abc"), then use eval()
    :param query: string
    :return: results: list
    """
    q = Query()
    # replace the operation name with the methods from Query class
    query = query.replace("EQUAL", "q.op_equal")
    query = query.replace("AND", "q.op_and")
    query = query.replace("OR", "q.op_or")
    query = query.replace("NOT", "q.op_not")
    query = query.replace("GREATER_THAN", "q.op_greater_than")
    query = query.replace("LESS_THAN", "q.op_less_than")
    # EQUAL(id,"abc") -> EQUAL("id","abc"), then it can be executed by eval()
    for case_name in sample_cases:
        for key in sample_cases[case_name]:
            if "\"" + key + "\"" not in query and "\'" + key + "\'" not in query:  # "id" or 'id' not in query
                query = query.replace(key, "\"" + key + "\"")  # id -> "id"
    try:
        # Restricting globals and locals
        query_condition = eval(query, {'__builtins__': None}, {"q": q})
        # print(query_condition)
        res = list(q.execute_query(query_condition))
    except:
        res = None
        LOG.error(traceback.format_exc())
    return res


if __name__ == '__main__':
    pq = ParseQuery()
    print(pq.parse_query_string(pq.pre_process_string("")))
    print(pq.parse_query_string(pq.pre_process_string('EQUAL(id,"first-post")')))
    print(pq.parse_query_string(pq.pre_process_string('EQUAL("id","abc")')))
    print(pq.parse_query_string(pq.pre_process_string('EQUAL(views,100)')))
    print(pq.parse_query_string(pq.pre_process_string('AND(EQUAL(id,"first-post"),EQUAL(views,100))')))
    print(pq.parse_query_string(pq.pre_process_string('AND(NOT(EQUAL(id,"first-post")),EQUAL(views,100))')))
    print(pq.parse_query_string(pq.pre_process_string('OR(EQUAL(id,"first-post"),EQUAL(id,"second-post"))')))
    print(pq.parse_query_string(pq.pre_process_string('NOT(EQUAL(id,"first-post"))')))
    print(pq.parse_query_string(pq.pre_process_string('GREATER_THAN(views,100)')))
    print(pq.parse_query_string(pq.pre_process_string('LESS_THAN(views,100)')))
    print(pq.parse_query_string(pq.pre_process_string('NOT(AND(EQUAL(id,"first-post"),EQUAL(id,"second-post")))')))
    print(pq.parse_query_string(pq.pre_process_string('NOT(AND(EQUAL(id,"first-post"),LESS_THAN(views,100)))')))
    print(pq.parse_query_string(pq.pre_process_string('NOT(OR(EQUAL(id,"third-post"),GREATER_THAN(views,100)))')))
    print(pq.parse_query_string(pq.pre_process_string('AND(NOT(OR(EQUAL(id,"third-post"),GREATER_THAN(views,100))),OR(EQUAL(id,"third-post"),EQUAL(id,"fourth-post")))')))
    print(pq.parse_query_string(pq.pre_process_string('AND(NOT(OR(EQUAL(id,"third-post"),GREATER_THAN(views,100))),EQUAL(id,"fourth-post"))')))
