FROM python:3.12-slim

# prevent python buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy the entire project
COPY . /app/

# # Expose port
# EXPOSE 8000

# Run Gunicorn using the wsgi module in sass_movie
CMD gunicorn sass_movie.wsgi:application --bind 0.0.0.0:8000 --workers 3