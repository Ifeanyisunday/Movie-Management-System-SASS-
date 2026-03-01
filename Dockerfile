FROM python:3.12-slim

# prevent python buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE=SASS_MOVIE.settings.prod

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy the entire project
COPY . /app/


# Run Gunicorn using the wsgi module in sass_movie
CMD gunicorn SASS_MOVIE.wsgi:application --bind 0.0.0.0:8000 --workers 3