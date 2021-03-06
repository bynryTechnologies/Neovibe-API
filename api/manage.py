#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()


def main():
    if env("smart360_env") == 'dev':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings.dev'

    if env("smart360_env") == 'qa':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings.prod'

    if env("smart360_env") == 'uat':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings.prod'

    if env("smart360_env") == 'prod':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings.prod'

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
