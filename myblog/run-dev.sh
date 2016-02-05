#!/bin/bash

set -e

. myblog/settings-dev.sh

./manage.py collectstatic --noinput
gunicorn myblog.wsgi
