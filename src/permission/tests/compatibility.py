# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
try:
    # from django 1.5
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

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
