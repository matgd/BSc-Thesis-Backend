#!/usr/bin/env bash
# REMEMBER TO KILL RUNNING UWSGI FIRST
set -e
# -- AS SU --
# systemctl stop ngnix
PROJECT_BASE_PATH='/usr/local/apps/soonmeet_api/soonmeet_api'

cd $PROJECT_BASE_PATH
# git pull
../env/bin/python manage.py migrate
../env/bin/python manage.py collectstatic --noinput
/usr/local/apps/soonmeet_api/env/bin/uwsgi --http :9000 --wsgi-file /local/apps/soonmeet_api/soonmeet_api/soonmeet_api/wsgi.py

echo "[  OK  ] Success!"
# -- AS SU --
# systemctl start nginx
