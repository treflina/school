import os
import sys
from urllib.parse import unquote

from django.core.wsgi import get_wsgi_application
from school.settings import base

sys.path.append(os.getcwd())
if base.DEBUG:
    os.environ['DJANGO_SETTINGS_MODULE'] = "school.settings.dev"
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = "school.settings.production"


def application(environ, start_response):
    environ["PATH_INFO"] = unquote(environ["PATH_INFO"]).encode('utf-8').decode('iso-8859-1')
    _application = get_wsgi_application()
    return _application(environ, start_response)