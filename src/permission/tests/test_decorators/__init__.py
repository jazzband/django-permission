import django
if django.VERSION < (1, 6):
    # Django 1.5 and earlier use a different test method and the followings
    # are required to be exposed
    from permission.tests.test_decorators.test_functionbase import *
    from permission.tests.test_decorators.test_methodbase import *
    from permission.tests.test_decorators.test_classbase import *
    from permission.tests.test_decorators.test_permission_required import *
