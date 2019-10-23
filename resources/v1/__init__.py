# coding=utf-8

from flask import Blueprint
from flask_cors import CORS

from application.response import Api
from utils import dynamic_import

version = "v1"
name = "api_{}".format(version)
url_prefix = "/api/{}".format(version)
api_blueprint = Blueprint(name, __name__, url_prefix=url_prefix)
api = Api(api_blueprint)

CORS(api_blueprint, origins="*")

Model = dynamic_import("models.{}".format(version))
Schema = dynamic_import("models.schema")


# allow import from *
__all__ = ["api", "Model", "Schema"]

# import api module
from . import resource_pack
from . import session