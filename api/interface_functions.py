# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/08/24
@description:
"""
from flask import request

from api.register_services import store_data, query_data


def api_hello():
    """
    :return:
    """
    return {"current_version": "V1.0.0"}


def api_store_data():
    """
    store the data from post request
    :return:
    """
    require_args = ["id", "title", "content", "views", "timestamp"]
    uid = request.form.get(require_args[0], "")
    title = request.form.get(require_args[1], "")
    content = request.form.get(require_args[2], "")
    views = request.form.get(require_args[3], 0)
    timestamp = request.form.get(require_args[4], 0)
    data = {
        require_args[0]: uid,
        require_args[1]: title,
        require_args[2]: content,
        require_args[3]: views,
        require_args[4]: timestamp
    }
    return store_data(data)


def api_query_data():
    """
    query the data from get request
    :return:
    """
    require_args = ["query"]
    query = request.args.get(require_args[0], "")
    return query_data(query)


if __name__ == '__main__':
    pass
