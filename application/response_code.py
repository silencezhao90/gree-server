# coding=utf-8
"""
    接口响应状态码
        0. 使用前必须在RegisterCode定义，否则报错!!!
        1. 错误响应码应该小于0
        2. 系统错误码取值范围-10001~-19999
        3. 业务错误码取值范围-20000~-99999(后期可分段使用)
"""
from enum import Enum, unique

__all__ = ("RegisterCode", "ErrorCode")

# 状态码注册,请同时添加注释
RegisterCode = [
    # 正常码
    10000,  # 正常,请求处理成功
    # 系统级错误代码
    -10000,  # 默认错误码
]


@unique
class ErrorCode(Enum):
    # 定义错误码
    pass
