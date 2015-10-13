# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
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
            MagicMock(get_supported_permissions=MagicMock(return_value=perms),
                      has_perm=MagicMock(return_value=False)),
            MagicMock(get_supported_permissions=MagicMock(return_value=perms),
                      has_perm=MagicMock(return_value=True)),
        ])

        backend = PermissionBackend()
        self.assertFalse(registry.get_handlers.called)
        self.assertFalse(registry.get_handlers()[0].get_supported_permissions.called)
        self.assertFalse(registry.get_handlers()[1].get_supported_permissions.called)
        self.assertFalse(registry.get_handlers()[0].has_perm.called)
        self.assertFalse(registry.get_handlers()[1].has_perm.called)

        self.assertTrue(backend.has_perm(self.user, self.perm1))

        self.assertTrue(registry.get_handlers.called)
        self.assertTrue(registry.get_handlers()[0].get_supported_permissions.called)
        self.assertTrue(registry.get_handlers()[1].get_supported_permissions.called)
        self.assertTrue(registry.get_handlers()[0].has_perm.called)
        self.assertTrue(registry.get_handlers()[1].has_perm.called)

    def test_has_perm_with_obj(self):
        perms = [
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ]
        registry.get_handlers = MagicMock(return_value=[
            MagicMock(get_supported_permissions=MagicMock(return_value=perms),
                      has_perm=MagicMock(return_value=False)),
            MagicMock(get_supported_permissions=MagicMock(return_value=perms),
                      has_perm=MagicMock(return_value=True)),
        ])

        backend = PermissionBackend()
        self.assertFalse(registry.get_handlers.called)
        self.assertFalse(registry.get_handlers()[0].get_supported_permissions.called)
        self.assertFalse(registry.get_handlers()[1].get_supported_permissions.called)
        self.assertFalse(registry.get_handlers()[0].has_perm.called)
        self.assertFalse(registry.get_handlers()[1].has_perm.called)

        self.assertTrue(backend.has_perm(self.user, self.perm1, self.article))

        self.assertTrue(registry.get_handlers.called)
        self.assertTrue(registry.get_handlers()[0].get_supported_permissions.called)
        self.assertTrue(registry.get_handlers()[1].get_supported_permissions.called)
        self.assertTrue(registry.get_handlers()[0].has_perm.called)
        self.assertTrue(registry.get_handlers()[1].has_perm.called)

    @override_settings(
        PERMISSION_CHECK_PERMISSION_PRESENCE=False,
    )
    def test_has_perm_with_nil_permission(self):
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
        self.assertFalse(backend.has_perm(None, 'permissions.nil_permission'))

    @override_settings(
        PERMISSION_CHECK_PERMISSION_PRESENCE=True,
    )
    def test_has_perm_with_nil_permission_raise(self):
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
        self.assertRaises(ObjectDoesNotExist,
                backend.has_perm,
                None, 'permissions.nil_permission')

    @override_settings(
        PERMISSION_CHECK_PERMISSION_PRESENCE=False,
        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'permission.backends.PermissionBackend',
        ),
    )
    def test_has_perm_with_nil_permission_with_user(self):
        self.assertFalse(self.user.has_perm('permissions.nil_permission'))

    @override_settings(
        PERMISSION_CHECK_PERMISSION_PRESENCE=True,
        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'permission.backends.PermissionBackend',
        ),
    )
    def test_has_perm_with_nil_permission_raise_with_user(self):
        self.assertRaises(ObjectDoesNotExist,
                self.user.has_perm,
                'permissions.nil_permission')

    def test_has_module_perms(self):
        perms = [
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ]
        app_labels = ['permission']
        registry.get_handlers = MagicMock(return_value=[
            MagicMock(get_supported_app_labels=MagicMock(return_value=app_labels),
                      has_module_perms=MagicMock(return_value=False)),
            MagicMock(get_supported_app_labels=MagicMock(return_value=app_labels),
                      has_module_perms=MagicMock(return_value=True)),
        ])

        backend = PermissionBackend()
        self.assertFalse(registry.get_handlers.called)
        self.assertFalse(registry.get_handlers()[0].get_supported_app_labels.called)
        self.assertFalse(registry.get_handlers()[1].get_supported_app_labels.called)
        self.assertFalse(registry.get_handlers()[0].has_module_perms.called)
        self.assertFalse(registry.get_handlers()[1].has_module_perms.called)

        self.assertTrue(backend.has_module_perms(self.user, 'permission'))

        self.assertTrue(registry.get_handlers.called)
        self.assertTrue(registry.get_handlers()[0].get_supported_app_labels.called)
        self.assertTrue(registry.get_handlers()[1].get_supported_app_labels.called)
        self.assertTrue(registry.get_handlers()[0].has_module_perms.called)
        self.assertTrue(registry.get_handlers()[1].has_module_perms.called)
