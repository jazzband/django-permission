# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
try:
    # Python 3 have mock in unittest
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

try:
    from django.test.utils import override_settings
except ImportError:
    from override_settings import override_settings

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

