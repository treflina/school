#!/usr/bin/env python
import os
import sys
from school.settings import base

if __name__ == "__main__":
    if base.DEBUG:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings.dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
