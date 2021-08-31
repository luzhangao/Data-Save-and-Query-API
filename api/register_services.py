# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description:
"""

from module.save_data import save_data_into_mongodb
from module.execute_query import exec_query
from config.error_code_map import *
from utils.decorator_tools import format_service_api_response


@format_service_api_response
def store_data(data):
    """
    call save function
    :param data: dict
           the dict to be saved
    :return: res, dict
    """
    res = dict()
    success = save_data_into_mongodb(data)
    if success:
        res["message"] = SAVE_DATA_SUCCESS
        res["error_code"] = code_map[SAVE_DATA_SUCCESS]
    else:
        res["message"] = FAILED_TO_INSERT
        res["error_code"] = code_map[FAILED_TO_INSERT]
    print(res)
    return res


@format_service_api_response
def query_data(query):
    """
    call specific query functions
    :param query: string
    :return: res, dict
    """
    res = dict()
    query_result = exec_query(query)
    if query_result["problem"] == "database problem":
        res["message"] = FAILED_TO_QUERY
        res["error_code"] = code_map[FAILED_TO_QUERY]
        res["data"] = []
    elif query_result["problem"] == "query string problem":
        res["message"] = PLEASE_ENTER_CORRECT_QUERY
        res["error_code"] = code_map[PLEASE_ENTER_CORRECT_QUERY]
        res["data"] = []
    else:
        res["message"] = QUERY_SUCCESS
        res["error_code"] = code_map[QUERY_SUCCESS]
        res["data"] = query_result["result"]

    return res


if __name__ == '__main__':
    pass
