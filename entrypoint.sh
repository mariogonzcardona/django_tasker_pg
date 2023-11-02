#!/bin/sh

echo 'Running collecstatic...'
python manage.py collectstatic --no-input --settings=django_tasker.settings.local

echo 'Ejecutando restore_db.py'
if [ "$DEBUG" = "True" ]; then
  echo 'Executing Python script...'
  # python restore_db.py
fi
# python manage.py makemigrations --settings=siarf.settings.local
# python manage.py migrate --settings=siarf.settings.local

# python manage.py loaddata ./fixtures/db.json --settings=siarf.settings.local

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=django_tasker.settings.local django_tasker.wsgi:application --bind 0.0.0.0:$PORT