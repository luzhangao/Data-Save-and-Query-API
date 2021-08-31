# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/08/24
@description:
"""

import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s %(levelname)s]: [%(module)s.%(funcName)s()]: %(message)s')

# Print logs if level > WARNING
logging.getLogger("requests").setLevel(logging.WARNING)

LOG = logging.getLogger()


if __name__ == "__main__":
    LOG.info("HELLO WORLD")
    LOG.debug("HELLO WORLD")
    LOG.error("error")








