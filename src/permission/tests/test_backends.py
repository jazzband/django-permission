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
from permission.utils.handlers import registry

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
        self.original_get_handlers = registry.get_handlers

    def tearDown(self):
        registry.get_handlers = self.original_get_handlers

    def test_constructor(self):
        backend = PermissionBackend()

    def test_authenticate(self):
        backend = PermissionBackend()
        self.assertEqual(backend.authenticate(None, None), None)

    def test_has_perm_without_obj(self):
        perms = [
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ]
        registry.get_handlers = MagicMock(return_value=[
            MagicMock(get_permissions=MagicMock(return_value=perms),
                      has_perm=MagicMock(return_value=False)),
            MagicMock(get_permissions=MagicMock(return_value=perms),
                      has_perm=MagicMock(return_value=True)),
        ])

        backend = PermissionBackend()
        self.assertFalse(registry.get_handlers.called)
        self.assertFalse(registry.get_handlers()[0].get_permissions.called)
        self.assertFalse(registry.get_handlers()[1].get_permissions.called)
        self.assertFalse(registry.get_handlers()[0].has_perm.called)
        self.assertFalse(registry.get_handlers()[1].has_perm.called)

        self.assertTrue(backend.has_perm(self.user, self.perm1))

        self.assertTrue(registry.get_handlers.called)
        self.assertTrue(registry.get_handlers()[0].get_permissions.called)
        self.assertTrue(registry.get_handlers()[1].get_permissions.called)
        self.assertTrue(registry.get_handlers()[0].has_perm.called)
        self.assertTrue(registry.get_handlers()[1].has_perm.called)

    def test_has_perm_with_obj(self):
        perms = [
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ]
        registry.get_handlers = MagicMock(return_value=[
            MagicMock(get_permissions=MagicMock(return_value=perms),
                      has_perm=MagicMock(return_value=False)),
            MagicMock(get_permissions=MagicMock(return_value=perms),
                      has_perm=MagicMock(return_value=True)),
        ])

        backend = PermissionBackend()
        self.assertFalse(registry.get_handlers.called)
        self.assertFalse(registry.get_handlers()[0].get_permissions.called)
        self.assertFalse(registry.get_handlers()[1].get_permissions.called)
        self.assertFalse(registry.get_handlers()[0].has_perm.called)
        self.assertFalse(registry.get_handlers()[1].has_perm.called)

        self.assertTrue(backend.has_perm(self.user, self.perm1, self.article))

        self.assertTrue(registry.get_handlers.called)
        self.assertTrue(registry.get_handlers()[0].get_permissions.called)
        self.assertTrue(registry.get_handlers()[1].get_permissions.called)
        self.assertTrue(registry.get_handlers()[0].has_perm.called)
        self.assertTrue(registry.get_handlers()[1].has_perm.called)

