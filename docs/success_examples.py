"""

doc blocks for success examples

"""


"""
@apiDefine SuccessTemplateResponse
@apiSuccessExample {json} Success-Response
    HTTP/1.1 200 OK
    {
        "code": 10000,
        "message": "success",
        "info": {
            "key1": "value1",
            "key2": "value2"
        },
        "list": {
            "pagination": {
                "total": 100,
                "limit": 20,
                "offset": 20
            },
            "data": [
                {
                    "key1": "value1"
                },
                {
                    "key2": "value2"
                }
            ]
        }
    }
"""

"""
@apiDefine SuccessDefaultResponse
@apiSuccessExample {json} Success-Response
    HTTP/1.1 200 OK
    {
        "code": 10000,
        "message": "success",
        "info": {},
        "list": {
            "pagination": false,
            "data": []
        }
    }
"""
