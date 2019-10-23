import sys
import os
import multiprocessing

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.dirname(path_of_current_file)

_file_name = os.path.splitext(os.path.basename(__file__))[0]

sys.path.insert(0, path_of_current_dir)

worker_class = "sync"
workers = multiprocessing.cpu_count() * 2 + 1

chdir = "/home/deploy/gree"

worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30
keepalive = 2

loglevel = "info"

reload = False

if not os.path.exists("%s/run" % (chdir)):
    os.makedirs("%s/run" % (chdir))

if not os.path.exists("%s/log" % (chdir)):
    os.makedirs("%s/log" % (chdir))

shared_path = chdir
bind = "%s:%s" % ("127.0.0.1", 8041)
pidfile = "%s/run/gunicorn.pid" % (shared_path)
errorlog = "%s/log/gunicorn_error.log" % (shared_path)
accesslog = "%s/log/gunicorn_access.log" % (shared_path)
