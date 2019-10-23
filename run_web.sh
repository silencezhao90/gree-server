#!/bin/sh

python3 manage.py db upgrade head
# gunicorn -c etc/gunicorn.py application:app
python3 manage.py runserver