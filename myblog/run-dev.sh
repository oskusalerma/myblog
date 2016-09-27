#!/bin/bash

set -e

. myblog/settings-dev.sh

./manage.py collectstatic --noinput
PYTHONWARNINGS=all gunicorn --reload --access-logfile - --access-logformat '%(t)s "%(r)s" %(s)s %(b)s' myblog.wsgi
