#!/bin/bash

set -e

. venv/bin/activate
cd myblog

. myblog/settings-dev.sh

./manage.py collectstatic --noinput
PYTHONWARNINGS=all gunicorn --reload --access-logfile - --access-logformat '%(t)s "%(r)s" %(s)s %(b)s' myblog.wsgi
