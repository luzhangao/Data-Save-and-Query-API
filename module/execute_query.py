# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description:
"""

import traceback
from module.parse_query import ParseQuery
from utils.log import LOG


def exec_query(query):
    """
    exec query
    :param query: string
    :return: dict {"result": [], "problem": ""}
    """
    result = {"result": [], "problem": []}
    pq = ParseQuery()
    std_query = pq.pre_process_string(query)  # pre process the query string
    mongodb_query = pq.parse_query_string(std_query)  # parse the query string and get the mongodb query dictionary
    if mongodb_query and not pq.is_error:  # mongodb_query can be dict or ""
        try:
            res = list(pq.execute_query(mongodb_query))
            result["result"] = res
        except:
            LOG.error(traceback.format_exc())
            result["problem"] = "database problem"
    else:  # ""
        result["problem"] = "query string problem"
    return result


if __name__ == '__main__':
    pass
