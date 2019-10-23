import hashlib
import importlib
import os

from hashlib import sha1
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage


def dynamic_import(package, attribute=None):
    module = importlib.import_module(package)
    if attribute is None:
        return module
    return getattr(module, attribute)


def get_params(arguments, strict=False):
    """获取参数解析"""
    parser = RequestParser()
    for argument in arguments:
        parser.add_argument(argument)
    values_dict = parser.parse_args(strict=strict)
    values = []
    for argument in arguments:
        values.append(values_dict.get(argument.name))
    return values


def generate_by_sha1_random():
    """ 产生一个随机的密文（消息摘要）
    :arg None
    :return 16位制的随机散列码
    """
    return sha1(os.urandom(24)).hexdigest()


def get_file_md5(file):
    md5 = None
    if isinstance(file, FileStorage):
        md5_obj = hashlib.md5()
        md5_obj.update(file.read())
        md5 = str(md5_obj.hexdigest()).lower()
        file.seek(0)

    return md5


def get_file_md5(file):
    md5 = None
    if isinstance(file, FileStorage):
        md5_obj = hashlib.md5()
        md5_obj.update(file.read())
        md5 = str(md5_obj.hexdigest()).lower()
        file.seek(0)

    return md5
