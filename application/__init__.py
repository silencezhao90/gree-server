# -*- coding:utf-8 -*-

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, ARCHIVES

settings_py = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "etc", "settings.py"
)

db = SQLAlchemy()

upload_resource = UploadSet('files', ARCHIVES)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(settings_py)

    # 文件存储地址
    app.config['UPLOADS_DEFAULT_DEST'] = os.getcwd()
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1000
    app.secret_key = app.config["SECRET_KEY"]
    db.init_app(app)
    configure_uploads(app, upload_resource)

    from resources.v1 import api_blueprint

    app.register_blueprint(api_blueprint)

    return app


app = create_app()
