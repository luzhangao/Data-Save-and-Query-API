# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description:
"""

import traceback
from utils.mongodb_util import *
from config.config import DB_test


def save_data_into_mongodb(data):
    """
    save the data into database
    :param data: dict
    :return: success: boolean
    """
    success = True
    try:
        db_connection = db_test(DB_test)
        db_connection.insert_one(data)
    except Exception as e:
        success = False
        LOG.error(traceback.format_exc())
    return success


if __name__ == '__main__':
    pass
