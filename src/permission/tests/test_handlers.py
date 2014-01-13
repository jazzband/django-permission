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
            u'permission.add_article',
            u'permission.change_article',
            u'permission.delete_article',
        ]))

    def test__get_app_perms_with_model(self):
        instance = self.handler(Article)
        perms = instance._get_app_perms()
        self.assertEquals(perms, set([
            u'permission.add_article',
            u'permission.change_article',
            u'permission.delete_article',
        ]))

    def test__get_model_perms(self):
        instance = self.handler(Article)
        perms = instance._get_model_perms()
        self.assertEquals(perms, set([
            u'permission.add_article',
            u'permission.change_article',
            u'permission.delete_article',
        ]))

    def test_get_permissions(self):
        instance = self.handler(Article)
        perms = instance.get_permissions(None, None)
        self.assertEquals(perms, set([
            u'permission.add_article',
            u'permission.change_article',
            u'permission.delete_article',
        ]))

    def test_get_permissions_with_includes(self):
        instance = self.handler(Article)
        instance.includes = [
                'permission.add_article',
                'permission.change_article',
            ]
        perms = instance.get_permissions(None, None)
        self.assertEquals(perms, set([
            u'permission.add_article',
            u'permission.change_article',
        ]))

    def test_get_permissions_with_includes_change(self):
        instance = self.handler(Article)
        instance.includes = [
                'permission.add_article',
                'permission.change_article',
            ]
        instance.get_permissions(None, None)
        instance.includes = [
                'permission.change_article',
            ]
        perms = instance.get_permissions(None, None)
        self.assertEquals(perms, set([
            u'permission.change_article',
        ]))


    def test_get_permissions_with_excludes(self):
        instance = self.handler(Article)
        instance.excludes = [
                'permission.add_article',
            ]
        perms = instance.get_permissions(None, None)
        self.assertEquals(perms, set([
            u'permission.change_article',
            u'permission.delete_article',
        ]))

    def test_get_permissions_with_excludes_change(self):
        instance = self.handler(Article)
        instance.excludes = [
                'permission.add_article',
            ]
        instance.get_permissions(None, None)
        instance.excludes = []
        perms = instance.get_permissions(None, None)
        self.assertEquals(perms, set([
            u'permission.add_article',
            u'permission.change_article',
            u'permission.delete_article',
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

@override_settings(
    PERMISSION_DEFAULT_PERMISSION_HANDLER=PermissionHandler
)
class PermissionLogicalPermissionHandlerTestCase(TestCase):
    def setUp(self):
        self.handler = LogicalPermissionHandler
        self.user = create_user('john')
        self.perm1 = 'permission.add_article'
        self.perm2 = 'permission.change_article'
        self.perm3 = 'permission.delete_article'
        self.article = create_article('test')

    def test_constructor_with_app_label(self):
        self.assertRaises(AttributeError,
                          self.handler, 'permission')
