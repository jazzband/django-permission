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
from permission.handlers import PermissionHandler
from permission.handlers import LogicalPermissionHandler
from permission.utils.handlers import PermissionHandlerRegistry

@override_settings(
    PERMISSION_DEFAULT_PERMISSION_HANDLER=PermissionHandler
)
class PermissionPermissionHandlersTestCase(TestCase):
    def setUp(self):
        self.handler = PermissionHandler
        self.user = create_user('john')
        self.perm1 = 'permission.add_article'
        self.perm2 = 'permission.change_article'
        self.perm3 = 'permission.delete_article'
        self.article = create_article('test')

    def test_constructor_with_model(self):
        instance = self.handler(Article)
        self.assertEqual(instance.app_label, 'permission')
        self.assertEqual(instance.model, Article)
        # backward reference
        self.assertEqual(Article._permission_handler, instance)

    def test_constructor_with_app_label(self):
        instance = self.handler('permission')
        self.assertEqual(instance.app_label, 'permission')
        self.assertEqual(instance.model, None)

    def test__get_app_perms_with_app_label(self):
        instance = self.handler('permission')
        perms = instance._get_app_perms()
        self.assertEquals(perms, set([
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
            'permission.add_bridge',
            'permission.change_bridge',
            'permission.delete_bridge',
        ]))

    def test__get_app_perms_with_model(self):
        instance = self.handler(Article)
        perms = instance._get_app_perms()
        self.assertEquals(perms, set([
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
            'permission.add_bridge',
            'permission.change_bridge',
            'permission.delete_bridge',
        ]))

    def test__get_model_perms(self):
        instance = self.handler(Article)
        perms = instance._get_model_perms()
        self.assertEquals(perms, set([
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ]))

    def test_get_supported_permissions(self):
        instance = self.handler(Article)
        perms = instance.get_supported_permissions()
        self.assertEquals(perms, set([
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ]))

    def test_get_supported_permissions_with_includes(self):
        instance = self.handler(Article)
        instance.includes = [
                'permission.add_article',
                'permission.change_article',
            ]
        perms = instance.get_supported_permissions()
        self.assertEquals(perms, set([
            'permission.add_article',
            'permission.change_article',
        ]))

    def test_get_supported_permissions_with_includes_change(self):
        instance = self.handler(Article)
        instance.includes = [
                'permission.add_article',
                'permission.change_article',
            ]
        instance.get_supported_permissions()
        instance.includes = [
                'permission.change_article',
            ]
        perms = instance.get_supported_permissions()
        self.assertEquals(perms, set([
            'permission.change_article',
        ]))


    def test_get_supported_permissions_with_excludes(self):
        instance = self.handler(Article)
        instance.excludes = [
                'permission.add_article',
            ]
        perms = instance.get_supported_permissions()
        self.assertEquals(perms, set([
            'permission.change_article',
            'permission.delete_article',
        ]))

    def test_get_supported_permissions_with_excludes_change(self):
        instance = self.handler(Article)
        instance.excludes = [
                'permission.add_article',
            ]
        instance.get_supported_permissions()
        instance.excludes = []
        perms = instance.get_supported_permissions()
        self.assertEquals(perms, set([
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ]))

    def test_get_supported_app_labels(self):
        instance = self.handler(Article)
        app_labels = instance.get_supported_app_labels()
        self.assertEquals(app_labels, set([
            'permission',
        ]))

    def test_get_supported_app_labels_with_includes(self):
        instance = self.handler(Article)
        instance.includes = [
                'permission.add_article',
                'permission.change_article',
            ]
        app_labels = instance.get_supported_app_labels()
        self.assertEquals(app_labels, set([
            'permission',
        ]))

    def test_get_supported_app_labels_with_includes_change(self):
        instance = self.handler(Article)
        instance.includes = [
                'permission.add_article',
                'permission.change_article',
            ]
        instance.get_supported_app_labels()
        instance.includes = [
                'permission.change_article',
            ]
        app_labels = instance.get_supported_app_labels()
        self.assertEquals(app_labels, set([
            'permission',
        ]))


    def test_get_supported_app_labels_with_excludes(self):
        instance = self.handler(Article)
        instance.excludes = [
                'permission.add_article',
            ]
        app_labels = instance.get_supported_app_labels()
        self.assertEquals(app_labels, set([
            'permission',
        ]))

    def test_get_supported_app_labels_with_excludes_change(self):
        instance = self.handler(Article)
        instance.excludes = [
                'permission.add_article',
            ]
        instance.get_supported_app_labels()
        instance.excludes = []
        app_labels = instance.get_supported_app_labels()
        self.assertEquals(app_labels, set([
            'permission',
        ]))

    def test_has_perm_add_wihtout_obj(self):
        instance = self.handler(Article)
        self.assertRaises(NotImplementedError,
                instance.has_perm,
                self.user, self.perm1)
        
    def test_has_perm_change_wihtout_obj(self):
        instance = self.handler(Article)
        self.assertRaises(NotImplementedError,
                instance.has_perm,
                self.user, self.perm2)

    def test_has_perm_delete_wihtout_obj(self):
        instance = self.handler(Article)
        self.assertRaises(NotImplementedError,
                instance.has_perm,
                self.user, self.perm3)

    def test_has_perm_add_wiht_obj(self):
        instance = self.handler(Article)
        self.assertRaises(NotImplementedError,
                instance.has_perm,
                self.user, self.perm1, self.article)

    def test_has_perm_change_wiht_obj(self):
        instance = self.handler(Article)
        self.assertRaises(NotImplementedError,
                instance.has_perm,
                self.user, self.perm2, self.article)

    def test_has_perm_delete_wiht_obj(self):
        instance = self.handler(Article)
        self.assertRaises(NotImplementedError,
                instance.has_perm,
                self.user, self.perm3, self.article)

    def test_has_module_perms_success(self):
        instance = self.handler(Article)
        user = MagicMock()
        user.has_perm.return_value = True
        self.assertTrue(instance.has_module_perms(user, 'permission'))
        self.assertTrue(user.has_perm.called)

    def test_has_module_perms_fail(self):
        instance = self.handler(Article)
        user = MagicMock()
        user.has_perm.return_value = True
        self.assertFalse(instance.has_module_perms(user, 'unknown'))
        self.assertFalse(user.has_perm.called)

@override_settings(
    PERMISSION_DEFAULT_PERMISSION_HANDLER=LogicalPermissionHandler
)
class PermissionLogicalPermissionHandlerTestCase(TestCase):
    def setUp(self):
        self.handler = LogicalPermissionHandler
        self.user = create_user('john')
        self.perm1 = 'permission.add_article'
        self.perm2 = 'permission.change_article'
        self.perm3 = 'permission.delete_article'
        self.article = create_article('test')

        from permission.logics import PermissionLogic
        from permission import add_permission_logic
        self.mock_logic1 = MagicMock(spec=PermissionLogic)
        self.mock_logic1.has_perm = MagicMock(return_value=False)
        self.mock_logic2 = MagicMock(spec=PermissionLogic)
        self.mock_logic2.has_perm = MagicMock(return_value=False)
        add_permission_logic(Article, self.mock_logic1)
        add_permission_logic(Article, self.mock_logic2)

    def test_constructor_with_app_label(self):
        self.assertRaises(AttributeError,
                          self.handler, 'permission')

    def test_has_perm_non_related_permission(self):
        instance = self.handler(Article)
        instance.get_supported_permissions = MagicMock(return_value=[
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ])
        self.assertFalse(instance.has_perm(self.user, 'unknown'))
        self.assertFalse(instance.has_perm(self.user, 'unknown', self.article))

    def test_has_perm_permission_logics_called(self):
        instance = self.handler(Article)
        instance.get_supported_permissions = MagicMock(return_value=[
            'permission.add_article',
            'permission.change_article',
            'permission.delete_article',
        ])
        self.assertFalse(self.mock_logic1.has_perm.called)
        self.assertFalse(self.mock_logic2.has_perm.called)
        self.assertFalse(instance.has_perm(self.user,
                                           'permission.add_article'))
        self.assertTrue(self.mock_logic1.has_perm.called)
        self.assertTrue(self.mock_logic2.has_perm.called)
        self.assertEqual(self.mock_logic1.has_perm.call_count, 1)
        self.assertEqual(self.mock_logic2.has_perm.call_count, 1)
        # permission check should be cached thus `has_perm` should not be
        # called twice for same user instance
        self.assertFalse(instance.has_perm(self.user,
                                           'permission.add_article'))
        self.assertEqual(self.mock_logic1.has_perm.call_count, 1)
        self.assertEqual(self.mock_logic2.has_perm.call_count, 1)
