# -*- coding:utf-8 -*-
import sys

from flask_script import Manager
from flask_script.commands import Server
from flask_migrate import Migrate, MigrateCommand

from application import db
from application import create_app

app = create_app()

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command("db", MigrateCommand)

manager.add_command("runserver", Server(
    host="0.0.0.0", port=8042, threaded=True))

if __name__ == "__main__":

    # print("[{command}]realibox app 开始运行".format(command=sys.argv[1]))

    manager.run()
