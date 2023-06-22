from .base import *

try:
    from .local import *
except ImportError:
    pass

DEBUG = True

with open(os.path.join(BASE_DIR, "secret.json")) as f:
    secret = json.loads(f.read())


def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = f"Nie mam dostępu do zmiennej {secret_name}"
        raise ImproperlyConfigured(msg)


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




