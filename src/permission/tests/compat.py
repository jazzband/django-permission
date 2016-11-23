# coding=utf-8
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from django.test import override_settings

try:
    from unittest import skipIf
except ImportError:
    def skipIf(condition, message):
        def decorator(f):
            return None if condition else f
        return decorator

from django.conf import settings
try:
    from django.test.runner import DiscoverRunner as TestRunnerBase
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner as TestRunnerBase

settings.TESTING = False
class TestRunner(TestRunnerBase):
    def setup_test_environment(self, **kwargs):
        super(TestRunner, self).setup_test_environment(**kwargs)
        settings.TESTING = True

    def teardown_test_environment(self, **kwargs):
        super(TestRunner, self).teardown_test_environment(**kwargs)
        settings.TESTING = False

try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    # python_2_unicode_compatible is ported from Django 1.5
    def python_2_unicode_compatible(cls):
        # Note:
        #   This project does not use any unicode literal so use __str__
        #   as __unicode__ works fine.
        cls.__unicode__ = cls.__str__
        return cls
