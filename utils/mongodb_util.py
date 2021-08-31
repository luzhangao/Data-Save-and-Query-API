# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/08/24
@description:
"""

import traceback
from pymongo import MongoClient
from pymongo import ReadPreference
from utils.log import LOG
from config.config import mongodb_database, sample_cases

db_pool = {}


class MongodbUtils(object):

    def __init__(self, collection, ip="", port=None, database='test', db_primary=False):
        self.ip = ip
        self.port = port
        self.database = database
        self.collection = collection
        self.db_primary = db_primary

        if (ip, port) not in db_pool:
            db_pool[(ip, port)] = self.db_connection()
        elif not db_pool[(ip, port)]:
            db_pool[(ip, port)] = self.db_connection()

        self.db = db_pool[(ip, port)]
        self.db_collection = self.db_collection_connect()

    def __enter__(self):
        return self.db_collection

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def db_connection(self):
        db = None
        try:
            if self.port:
                db = MongoClient(self.ip, self.port)
            else:
                if self.db_primary:
                    db = MongoClient(self.ip, read_preference=ReadPreference.PRIMARY_PREFERRED)
                else:
                    db = MongoClient(self.ip, read_preference=ReadPreference.SECONDARY_PREFERRED)
        except Exception as e:
            # print(e)
            LOG.error(traceback.format_exc())
        return db

    def db_collection_connect(self):
        collection_db = self.db[self.database][self.collection]
        return collection_db


def db_data(db_type):
    """
    Get the database information from config
    :param db_type: string
    :return: (ip, port, database and collection): tuple
    """
    rpt_dict = mongodb_database[db_type]
    return rpt_dict["DB_IP"], rpt_dict["DB_PORT"], rpt_dict["DB_DATABASE"], rpt_dict["DB_COLLECTION"]


def db_test(data_type="DeviantArt"):
    """
    Connect to the database
    :param data_type: string
    :return: database connection
    """
    monitor_ip, monitor_port, database, collection = db_data(data_type)
    db_monitor = MongodbUtils(ip=monitor_ip, port=monitor_port, database=database, collection=collection)
    return db_monitor.db_collection


if __name__ == '__main__':
    t = db_test()
    for case in sample_cases:
        # t.insert_one(sample_cases[case])
        t.delete_one(sample_cases[case])

