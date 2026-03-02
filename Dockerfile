FROM python:3.12-slim

# prevent python buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Copy the entire project
COPY . .

ENV DJANGO_SETTINGS_MODULE=SASS_MOVIE.settings.prod

ENV PORT=8000

EXPOSE 8000

# Run Gunicorn using the wsgi module in sass_movie
CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn SASS_MOVIE.wsgi:application --bind 0.0.0.0:$PORT