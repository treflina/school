from .base import *


ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")

SECRET_KEY = get_secret("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_secret("DB_NAME"),
        "USER": get_secret("DB_USER"),
        "PASSWORD": get_secret("DB_PASSWORD"),
        "HOST": "127.0.0.1",
        "PORT": "",
    }
}