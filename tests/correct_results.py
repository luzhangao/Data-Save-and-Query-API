# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/8/25
@description: cases for testing
"""

from config.config import sample_cases

# insert data cases, the response of the key should equals value
insert_cases = {
    str(sample_cases["case1"]): {"status": "200", "result": {"message": "save the data into database successfully",
                                                             "error_code": 31200}},
    str(sample_cases["case2"]): {"status": "200", "result": {"message": "save the data into database successfully",
                                                             "error_code": 31200}},
    str(sample_cases["case3"]): {"status": "200", "result": {"message": "save the data into database successfully",
                                                             "error_code": 31200}},
    str(sample_cases["case4"]): {"status": "200", "result": {"message": "save the data into database successfully",
                                                             "error_code": 31200}},
    str(sample_cases["case5"]): {"status": "200", "result": {"message": "save the data into database successfully",
                                                             "error_code": 31200}},
}

# query data cases, the response of the key should equals value
query_cases = {
    # simple correct cases
    str({"query": 'EQUAL(id,"first-post")'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World!',
                            'id': 'first-post',
                            'timestamp': 1558322341,
                            'title': 'My First Post',
                            'views': 1
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'EQUAL(id,"abc")'}): {
        'result':
            {
                'data': [],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'EQUAL(views,100)'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World 2!',
                            'id': 'second-post',
                            'timestamp': 1558322342,
                            'title': 'My Second Post',
                            'views': 100
                        },
                        {
                            'content': 'Hello World 3!',
                            'id': 'third-post',
                            'timestamp': 1558322343,
                            'title': 'My Third Post',
                            'views': 100
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'AND(EQUAL(id,"second-post"),EQUAL(views,100))'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World 2!',
                            'id': 'second-post',
                            'timestamp': 1558322342,
                            'title': 'My Second Post',
                            'views': 100
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'OR(EQUAL(id,"second-post"),EQUAL(views,100))'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World 2!',
                            'id': 'second-post',
                            'timestamp': 1558322342,
                            'title': 'My Second Post',
                            'views': 100
                        },
                        {
                            'content': 'Hello World 3!',
                            'id': 'third-post',
                            'timestamp': 1558322343,
                            'title': 'My Third Post',
                            'views': 100
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'NOT(EQUAL(id,"first-post"))'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World 2!',
                            'id': 'second-post',
                            'timestamp': 1558322342,
                            'title': 'My Second Post',
                            'views': 100
                        },
                        {
                            'content': 'Hello World 3!',
                            'id': 'third-post',
                            'timestamp': 1558322343,
                            'title': 'My Third Post',
                            'views': 100
                        },
                        {
                            'content': 'Hello World 4!',
                            'id': 'fourth-post',
                            'timestamp': 1558322344,
                            'title': 'My Fourth Post',
                            'views': 1000},
                        {
                            'content': 'Hello World 5!',
                            'id': 'fifth-post',
                            'timestamp': 1558322341,
                            'title': 'My Fifth Post',
                            'views': 50
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'GREATER_THAN(views,100)'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World 4!',
                            'id': 'fourth-post',
                            'timestamp': 1558322344,
                            'title': 'My Fourth Post',
                            'views': 1000},
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'LESS_THAN(views,100)'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World!',
                            'id': 'first-post',
                            'timestamp': 1558322341,
                            'title': 'My First Post',
                            'views': 1
                        },
                        {
                            'content': 'Hello World 5!',
                            'id': 'fifth-post',
                            'timestamp': 1558322341,
                            'title': 'My Fifth Post',
                            'views': 50
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    # complex correct cases
    str({"query": 'NOT(AND(EQUAL(id,"first-post"),EQUAL(id,"second-post")))'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World!',
                            'id': 'first-post',
                            'timestamp': 1558322341,
                            'title': 'My First Post',
                            'views': 1
                        },
                        {
                            'content': 'Hello World 2!',
                            'id': 'second-post',
                            'timestamp': 1558322342,
                            'title': 'My Second Post',
                            'views': 100
                        },
                        {
                            'content': 'Hello World 3!',
                            'id': 'third-post',
                            'timestamp': 1558322343,
                            'title': 'My Third Post',
                            'views': 100
                        },
                        {
                            'content': 'Hello World 4!',
                            'id': 'fourth-post',
                            'timestamp': 1558322344,
                            'title': 'My Fourth Post',
                            'views': 1000},
                        {
                            'content': 'Hello World 5!',
                            'id': 'fifth-post',
                            'timestamp': 1558322341,
                            'title': 'My Fifth Post',
                            'views': 50
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'NOT(OR(EQUAL(id,"third-post"),GREATER_THAN(views,100)))'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World!',
                            'id': 'first-post',
                            'timestamp': 1558322341,
                            'title': 'My First Post',
                            'views': 1
                        },
                        {
                            'content': 'Hello World 2!',
                            'id': 'second-post',
                            'timestamp': 1558322342,
                            'title': 'My Second Post',
                            'views': 100
                        },
                        {
                            'content': 'Hello World 5!',
                            'id': 'fifth-post',
                            'timestamp': 1558322341,
                            'title': 'My Fifth Post',
                            'views': 50
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    str({"query": 'OR(NOT(EQUAL(id,"third-post")), GREATER_THAN(views,100)))'}): {
        'result':
            {
                'data':
                    [
                        {
                            'content': 'Hello World!',
                            'id': 'first-post',
                            'timestamp': 1558322341,
                            'title': 'My First Post',
                            'views': 1
                        },
                        {
                            'content': 'Hello World 2!',
                            'id': 'second-post',
                            'timestamp': 1558322342,
                            'title': 'My Second Post',
                            'views': 100
                        },
                        {
                            'content': 'Hello World 4!',
                            'id': 'fourth-post',
                            'timestamp': 1558322344,
                            'title': 'My Fourth Post',
                            'views': 1000},
                        {
                            'content': 'Hello World 5!',
                            'id': 'fifth-post',
                            'timestamp': 1558322341,
                            'title': 'My Fifth Post',
                            'views': 50
                        }
                    ],
                'error_code': 31200,
                'message': 'query the data successfully'
            },
        'status': '200'
    },
    # wrong cases
    str({"query": 'GGG(views,100)'}): {
        'result':
            {
                'data': [],
                'error_code': 31204,
                'message': 'please send correct query strings'
            },
        'status': '200'
    },
    str({"query": 'GREATER_THAN(views, "100")'}): {
        'result':
            {
                'data': [],
                'error_code': 31204,
                'message': 'please send correct query strings'
            },
        'status': '200'
    },
    str({"query": 'LESS_THAN(views, "100K")'}): {
        'result':
            {
                'data': [],
                'error_code': 31204,
                'message': 'please send correct query strings'
            },
        'status': '200'
    },
}

if __name__ == '__main__':
    print(insert_cases[str(sample_cases["case1"])])
