from .base import *

DEBUG = True

SECRET_KEY = "dev-secret-key"

ALLOWED_HOSTS = ["*"]


# Local database (Postgres or SQLite)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Dev cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}


# CORS for local frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

CORS_ALLOW_ALL_ORIGINS = False
