# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/24
@description: the current configuration
"""

DB_test = "DeviantArt"

mongodb_database = {
    "DeviantArt": {
        "DB_IP": "localhost",
        "DB_PORT": 27017,
        "DB_DATABASE": "DeviantArt",
        "DB_COLLECTION": "Entity"
    }
}

# samples from the post request
sample_cases = {
    "case1": {
        "id": "first-post",
        "title": "My First Post",
        "content": "Hello World!",
        "views": 1,
        "timestamp": 1558322341
    },
    "case2": {
        "id": "second-post",
        "title": "My Second Post",
        "content": "Hello World 2!",
        "views": 100,
        "timestamp": 1558322342
    },
    "case3": {
        "id": "third-post",
        "title": "My Third Post",
        "content": "Hello World 3!",
        "views": 100,
        "timestamp": 1558322343
    },
    "case4": {
        "id": "fourth-post",
        "title": "My Fourth Post",
        "content": "Hello World 4!",
        "views": 1000,
        "timestamp": 1558322344
    },
    "case5": {
        "id": "fifth-post",
        "title": "My Fifth Post",
        "content": "Hello World 5!",
        "views": 50,
        "timestamp": 1558322341
    },
}


if __name__ == '__main__':
    pass
