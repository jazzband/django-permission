# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from permission.tests.compatibility import MagicMock
from permission.tests.compatibility import override_settings
from permission.handlers import PermissionHandler
from permission.utils.handlers import PermissionHandlerRegistry

@override_settings(
    PERMISSION_DEFAULT_PERMISSION_HANDLER=PermissionHandler
)
class PermissionUtilsHandlersTestCase(TestCase):
    def setUp(self):
        self.registry = PermissionHandlerRegistry()
        self.model = MagicMock()
        self.model._meta = MagicMock()
        self.model._meta.abstract = False
        self.handler = PermissionHandler

    def test_register(self):
        self.registry.register(self.model, self.handler)
        self.assertTrue(self.model in self.registry._registry)
        self.assertTrue(isinstance(self.registry._registry[self.model],
                                   self.handler))

    def test_register_without_specifing_handler(self):
        self.registry.register(self.model)
        self.assertTrue(self.model in self.registry._registry)
        self.assertTrue(isinstance(self.registry._registry[self.model],
                                   self.handler))

    def test_register_with_abstract_model(self):
        from django.core.exceptions import ImproperlyConfigured
        abstract_model = MagicMock()
        abstract_model._meta = MagicMock()
        abstract_model._meta.abstract = True
        self.assertRaises(ImproperlyConfigured,
                          self.registry.register,
                          abstract_model, self.handler)

    def test_register_duplicate(self):
        self.registry.register(self.model, self.handler)
        self.assertRaises(KeyError,
                          self.registry.register,
                          self.model, self.handler)

    def test_register_permission_handler_instance(self):
        handler_instance = self.handler(self.model)
        self.assertRaises(AttributeError,
                          self.registry.register,
                          self.model, handler_instance)

    def test_register_non_permission_handler(self):
        self.assertRaises(AttributeError,
                          self.registry.register,
                          self.model, self.__class__)

    def test_unregister(self):
        self.registry.register(self.model, self.handler)
        self.registry.unregister(self.model)
        self.assertFalse(self.model in self.registry._registry)

    def test_unregister_absence(self):
        self.assertRaises(KeyError,
                          self.registry.unregister,
                          self.model)

    def test_get_handlers(self):
        results = self.registry.get_handlers()
        self.assertTrue(isinstance(results, tuple))
        self.assertTrue(len(results) == 0)

        self.registry.register(self.model, self.handler)
        results = self.registry.get_handlers()
        self.assertTrue(isinstance(results, tuple))
        self.assertTrue(len(results) == 1)
        self.assertTrue(isinstance(results[0], PermissionHandler))

