from collections import OrderedDict
from flask_restful import Api as BaseApi
from werkzeug.exceptions import HTTPException

from application.response_code import RegisterCode, ErrorCode


class Api(BaseApi):

    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)

    def make_response(self, data, *args, **kwargs):
        """
            统一接口正常响应格式
        """
        if not isinstance(data, Response):
            raise ValueError("接口返回数据格式不符合规范")
        resp = data

        response = super(Api, self).make_response(resp.response, *args, **kwargs)
        if resp.customize and isinstance(resp.customize, dict):
            func = resp.customize.get("func")
            param = resp.customize.get("param")
            getattr(response, func)(**param)

        return response

    def handle_error(self, e):
        """
            统一接口异常响应格式
        """
        http_code = 200

        # 异常处理
        if isinstance(e, ResponseError):
            resp = e.box_response
            return super(Api, self).make_response(resp.response, http_code)

        # 参数检查等
        data = getattr(e, "data", None)
        if data:
            message = self.collect_msg(data.pop("message", None))
            resp = Response(code=-10001, message=message)
            return super(Api, self).make_response(resp.response, http_code)

        return super(Api, self).handle_error(e)

    @staticmethod
    def collect_msg(message_dict):
        s = ""
        for key, value in message_dict.items():
            s += 'parameter "%s" is %s' % (key, value)
        return s


class Response(object):
    """
        Api Response
        eg.
            {
                "code": 1000,
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

    def __init__(self, **kwargs):
        self.code = int(kwargs.get("code", 10000))
        self.message = kwargs.get("message", "success")
        self.info = kwargs.get("info", dict())
        self.data = kwargs.get("data", list())
        self.pagination = kwargs.get("pagination", False)
        self.customize = kwargs.get("customize", False)
        if self.pagination is True:
            self.pagination = dict(
                total=int(kwargs["total"]),
                limit=int(kwargs["limit"]),
                offset=int(kwargs["offset"]),
            )

    @property
    def response(self):
        resp = OrderedDict()
        if self.code not in RegisterCode:
            raise ValueError("返回码未注册")
        resp["code"] = self.code
        resp["message"] = self.message
        if self.code > 0:
            resp["info"] = self.info
            resp["list"] = dict(pagination=self.pagination, data=self.data)
        return resp


class ResponseError(HTTPException):
    """
        新版接口的异常处理方案
        eg:
            raise BoxError('UserNameAlreadyExists')
    """

    def __init__(self, error="", info=None):
        errobj = getattr(ErrorCode, error, None)
        self.box_response = Response(code=-10000)
        if info:
            self.box_response.message = info
        elif errobj is None:
            self.box_response.code = -10005
            self.box_response.message = "接口错误代码未定义"
        else:
            self.box_response.code = errobj.value.get("code")
            self.box_response.message = errobj.value.get("desc")
        super(ResponseError, self).__init__()
