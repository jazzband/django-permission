# coding=utf-8
"""
Django 1.2 - 1.6 compatible manage.py
Modify this script to make your own manage.py
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import sys


if __name__ == '__main__':
    # add extra sys.path
    root = os.path.abspath(os.path.dirname(__file__))
    extra_paths = (root, os.path.join(root, 'src'))
    for extra_path in extra_paths:
        if extra_path in sys.path:
            sys.path.remove(extra_path)
        sys.path.insert(0, extra_path)
    # set DJANGO_SETTINGS_MODULE
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

    try:
        # django 1.4 and above
        # https://docs.djangoproject.com/en/1.4/releases/1.4/
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError:
        from django.core.management import execute_manager
        settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'])
        execute_manager(settings)
