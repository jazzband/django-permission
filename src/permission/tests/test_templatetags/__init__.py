import django
if django.VERSION < (1, 6):
    # Django 1.5 and earlier use a different test method and the followings
    # are required to be exposed
    from permission.tests.test_templatetags.test_permissionif import *
