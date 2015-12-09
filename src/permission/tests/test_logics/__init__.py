import django
if django.VERSION < (1, 6):
    # Django 1.5 and earlier use a different test method and the followings
    # are required to be exposed
    from permission.tests.test_logics.test_base import *
    from permission.tests.test_logics.test_author import *
    from permission.tests.test_logics.test_collaborators import *
    from permission.tests.test_logics.test_groupin import *
    from permission.tests.test_logics.test_staff import *
    from permission.tests.test_logics.test_oneself import *
