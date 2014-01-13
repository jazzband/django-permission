# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from permission.tests.utils import create_user
from permission.tests.utils import create_article
from permission.tests.models import Article
from permission.tests.compatibility import MagicMock
from permission.tests.compatibility import override_settings
from permission.backends import PermissionBackend

@override_settings(
    AUTHENTICATION_BACKENDS=(
        'django.contrib.auth.backends.ModelBackend',
        'permission.backends.PermissionBackend',
    ),
)
class PermissionPermissionBackendTestCase(TestCase):
    def setUp(self):
        self.user = create_user('john')
        self.perm1 = 'permission.add_article'
        self.perm2 = 'permission.change_article'
        self.perm3 = 'permission.delete_article'
        self.article = create_article('test')

    def test_constructor(self):
        backend = PermissionBackend()

    def test_authenticate(self):
        backend = PermissionBackend()
        self.assertEqual(backend.authenticate(None, None), None)
