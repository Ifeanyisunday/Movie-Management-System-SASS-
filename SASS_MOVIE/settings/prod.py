from .base import *
import os
import dj_database_url


DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


# Render Postgres
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600
    )
}


# Redis cache (optional but recommended)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}


# Production CORS (adjust later for frontend domain)
CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_ALL_ORIGINS = False


# Production security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
