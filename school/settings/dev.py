import os
from .base import *

SECRET_KEY = "django-insecure-zuue#^e0hzleqj8r+7@tk%z$oygg9cg6ldwfmh#qdny*ko%b4m"

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"