# coding=utf-8
"""
    Flask app settings
"""

# For flask
# HOST = "local.enterprise.realibox.com"
# SERVER_NAME = "local.enterprise.realibox.com"
DEBUG = True
SECRET_KEY = "\xa0+\x04i3V\x8b\xa0\xc3g\xe7\xa5S\xb5%\x07x\xe0K\xb0?a\xa2\x15"

# For flask-sqlalchemy
SQLALCHEMY_ECHO = False
# SQLALCHEMY_DATABASE_URI = "postgres://gree:123456@127.0.0.1/gree"
SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@db/postgres"

# For flask_restful
RESTFUL_JSON = {"sort_keys": False}


SERVER_URL = 'http://gree.esun3dcloud.com'
STATIC_SERVER_URL = 'http://static.gree.esun3dcloud.com'
