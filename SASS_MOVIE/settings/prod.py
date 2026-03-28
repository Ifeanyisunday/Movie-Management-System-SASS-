from .base import *
import os
import dj_database_url


DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", 
                          "movie-api-53sv.onrender.com"
                          ).split(",")


# Render Postgres
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600
    )
}

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}


CORS_ALLOWED_ORIGINS = [
    "https://movie-management-system-sass-fronte.vercel.app",
]

CORS_ALLOW_ALL_ORIGINS = False


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True


