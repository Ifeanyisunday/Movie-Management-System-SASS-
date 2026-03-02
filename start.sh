#!/bin/sh

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn on port $PORT..."
exec gunicorn SASS_MOVIE.wsgi:application --bind 0.0.0.0:$PORT