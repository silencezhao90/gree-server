from flask import request
from flask_restful import Resource
from flask_restful.reqparse import Argument

from application.response import Response, ResponseError
from resources.v1 import api
from utils import get_params


@api.resource('/session/login')
class LoginResource(Resource):
    def post(self):
        (username, password, ) = get_params([
            Argument('username', type=str, required=True),
            Argument('password', type=str, required=True),
        ])

        if username == 'admin' and password == '123456':
            return Response()
        raise ResponseError(info='账号密码错误!')

