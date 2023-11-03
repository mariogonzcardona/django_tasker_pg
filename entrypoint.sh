#!/bin/sh

echo 'Running collecstatic...'
python manage.py collectstatic --no-input --settings=django_tasker.settings.local

echo 'Ejecutando restore_db.py'
if [ "$DEBUG" = "True" ]; then
  echo 'Executing Python script...'
  python ./sql_commands/restore_db.py
fi
python manage.py makemigrations --settings=django_tasker.settings.local
python manage.py migrate --settings=django_tasker.settings.local

python manage.py loaddata ./fixtures/full_db.json --settings=django_tasker.settings.local

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=django_tasker.settings.local django_tasker.wsgi:application --bind 0.0.0.0:$PORT