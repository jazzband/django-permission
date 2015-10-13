# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from permission.tests.models import Article
from permission.tests.compatibility import MagicMock
from permission.logics import PermissionLogic
from permission.handlers import LogicalPermissionHandler
from permission.utils.handlers import registry
from permission.utils.logics import add_permission_logic
from permission.utils.logics import remove_permission_logic


class PermissionUtilsLogicsTestCase(TestCase):
    def setUp(self):
        self.mock_logic = MagicMock(spec=PermissionLogic)
        self.mock_logic2 = MagicMock(spec=PermissionLogic)
        # clear registry
        self.registry_backup = registry._registry
        registry._registry = {}
        # clear attributes
        if hasattr(Article, '_permission_logics'):
            delattr(Article, '_permission_logics')
        if hasattr(Article, '_permission_handler'):
            delattr(Article, '_permission_handler')

    def tearDown(self):
        registry._registry = self.registry_backup

    def test_add_permission_logic_private_attributes(self):
        m = self.mock_logic
        # the following private attribute should not be exists in Article model
        self.assertFalse(hasattr(Article, '_permission_logics'))
        self.assertFalse(hasattr(Article, '_permission_handler'))

        # but after add permission logic, they will be appeared
        add_permission_logic(Article, m)
        self.assertTrue(hasattr(Article, '_permission_logics'))
        self.assertTrue(hasattr(Article, '_permission_handler'))
    
    def test_add_permission_logic_registry(self):
        m = self.mock_logic
        # nothing have been registered in registry
        self.assertEqual(registry._registry, {})
        # but after add permission logic, they will be appeared
        add_permission_logic(Article, m)
        self.assertEqual(Article._permission_logics, set([m]))
        self.assertTrue(isinstance(registry._registry[Article],
                                   LogicalPermissionHandler))

    def test_remove_permission_logic_private_attributes(self):
        m = self.mock_logic
        add_permission_logic(Article, m)
        self.assertTrue(hasattr(Article, '_permission_logics'))
        self.assertTrue(hasattr(Article, '_permission_handler'))

        # private attribute should not be disappeared
        remove_permission_logic(Article, m)
        self.assertTrue(hasattr(Article, '_permission_logics'))
        self.assertTrue(hasattr(Article, '_permission_handler'))
    
    def test_remove_permission_logic_registry(self):
        m = self.mock_logic
        add_permission_logic(Article, m)
        self.assertEqual(Article._permission_logics, set([m]))
        self.assertTrue(isinstance(registry._registry[Article],
                                   LogicalPermissionHandler))

        # permission_logics should be changed but registry
        # should not be changed
        remove_permission_logic(Article, m)
        self.assertEqual(Article._permission_logics, set())
        self.assertTrue(isinstance(registry._registry[Article],
                                   LogicalPermissionHandler))

    def test_remove_permission_logic_registry_with_class(self):
        m = self.mock_logic
        m2 = self.mock_logic2
        add_permission_logic(Article, m)
        add_permission_logic(Article, m2)
        self.assertEqual(Article._permission_logics, set([m, m2]))
        self.assertTrue(isinstance(registry._registry[Article],
                                   LogicalPermissionHandler))

        # permission_logics should be changed but registry
        # should not be changed
        remove_permission_logic(Article, PermissionLogic)
        self.assertEqual(Article._permission_logics, set())
        self.assertTrue(isinstance(registry._registry[Article],
                                   LogicalPermissionHandler))

    def test_remove_permission_logic_exception(self):
        m = self.mock_logic
        add_permission_logic(Article, m)
        remove_permission_logic(Article, m)
        # it shuld not raise exception
        remove_permission_logic(Article, m)
        # it should raise exception if fail_silently is False
        self.assertRaises(KeyError,
                remove_permission_logic, Article, m,
                fail_silently=False)
