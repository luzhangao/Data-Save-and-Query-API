# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description:
"""

from flask import Flask

from api.interface_functions import *
from utils.decorator_tools import response_json

app = Flask(__name__)


@app.route("/")
@response_json
def hello():
    """
    first API
    :return: json
    """
    return api_hello()


@app.route('/store', methods=['GET', 'POST'])
@response_json
def sentiment():
    """
    :return: json
    """
    res = dict()
    if request.method == "POST":
        res = api_store_data()
    else:
        res = api_query_data()
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)

