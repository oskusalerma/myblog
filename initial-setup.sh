#!/bin/bash

virtualenv venv
. venv/bin/activate
pip install -U pip
pip install Django
pip install psycopg2
pip install dj-database-url
