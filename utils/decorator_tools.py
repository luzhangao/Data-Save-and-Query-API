# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description:
"""


import json
from functools import wraps
from flask import Response


def response_json(func):
    """
    return JSON
    Content-Type=application/json
    charset=utf-8
    :param func: function
    :return: json
    """

    @wraps(func)
    def set_response(*args, **kwargs):
        res = func(*args, **kwargs)
        if type(res) is not dict:
            return res
        else:
            return Response(json.dumps(res), content_type="application/json; charset=utf-8")
    return set_response


def format_service_api_response(func):
    """
    format the API response
    :param func: function
    :return: dict
    """
    @wraps(func)
    def get_response(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return {"status": "200", "result": res}
        except:
            return {"status": "404", "result": ""}
    return get_response


if __name__ == '__main__':
    pass
