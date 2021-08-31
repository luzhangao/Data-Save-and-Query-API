# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description: list all possible error codes
"""

# 200
SAVE_DATA_SUCCESS = "save the data into database successfully"
QUERY_SUCCESS = "query the data successfully"
# 204
PLEASE_ENTER_CORRECT_QUERY = "please send correct query strings"
# 500
FAILED_TO_INSERT = "failed to insert the data into database"
FAILED_TO_QUERY = "failed to query the database"


code_map = {
    # 200
    SAVE_DATA_SUCCESS: 31200,
    QUERY_SUCCESS: 31200,
    # 204
    PLEASE_ENTER_CORRECT_QUERY: 31204,
    # 500
    FAILED_TO_INSERT: 31500,
    FAILED_TO_QUERY: 31500,
}


if __name__ == '__main__':
    pass
