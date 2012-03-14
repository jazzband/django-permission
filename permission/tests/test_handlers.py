# vim: set fileencoding=utf-8 :
"""
Unittest module of ...


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
License:
    The MIT License (MIT)

    Copyright (c) 2012 Alisue allright reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.

"""
from __future__ import with_statement
from django.test import TestCase
from django.contrib.auth.models import Permission

from permission import PermissionHandler
from permission.exceptions import ValidationError
from permission.tests.models import Article
try:
    from django.test.utils import override_settings
except ImportError:
    from override_settings import override_settings

class PermissionHandlerTestCase(TestCase):

    def test_registry_instance(self):
        from permission.handlers import Registry
        from permission import registry

        self.assertTrue(isinstance(registry, Registry))

    def test_registry_register(self):
        from permission.handlers import Registry
        from permission.exceptions import AlreadyRegistered
        registry = Registry()
        registry.register(Article, PermissionHandler)

        self.assertEqual(len(registry._registry), 1)
        self.assertTrue(isinstance(
                registry._registry[Article], 
                PermissionHandler
            ))

        # duplicate entry should raise AlreadyRegistered
        self.assertRaises(
                AlreadyRegistered,
                registry.register,
                Article, PermissionHandler
            )

    def test_registry_register_validation(self):
        class Mock(object):
            pass
        from permission.handlers import Registry
        registry = Registry()

        with override_settings(DEBUG=True):
            # model must be a subclass of Model
            self.assertRaises(
                    ValidationError,
                    registry.register,
                    Mock, PermissionHandler
                )
            # handler must be a subclass of PermissionHandler
            self.assertRaises(
                    ValidationError,
                    registry.register,
                    Article, Mock,
                )

        # validation should not be happen in DEBUG=False
        with override_settings(DEBUG=False):
            # Insted of ValidationError, AttributeError will raise
            # which mean the models have not validated
            self.assertRaises(
                    AttributeError,
                    registry.register,
                    Mock, PermissionHandler
                )
            # Insted of ValidationError, TypeError will raise
            # which mean the handler have not validated
            self.assertRaises(
                    TypeError,
                    registry.register,
                    Article, Mock
                )

    def test_registry_unregister(self):
        from permission.handlers import Registry
        from permission.exceptions import NotRegistered
        registry = Registry()
        registry.register(Article, PermissionHandler)

        registry.unregister(Article)
        self.assertEqual(len(registry._registry), 0)

        # non registered entry should raise NotRegistered
        self.assertRaises(NotRegistered, registry.unregister, Article)

    def test_registry_get_handlers(self):
        from permission.handlers import Registry
        registry = Registry()
        registry.register(Article, PermissionHandler)

        handlers = registry.get_handlers('permission.add_article')
        self.assertTrue(isinstance(handlers, tuple))
        self.assertEqual(len(handlers), 1)
        self.assertEqual(handlers[0].__class__, PermissionHandler)

        # not registered
        handlers = registry.get_handlers('auth.add_user')
        self.assertTrue(isinstance(handlers, tuple))
        self.assertEqual(len(handlers), 0)

        # unknown
        handlers = registry.get_handlers('not_registered_app.unknown_model')
        self.assertTrue(isinstance(handlers, tuple))
        self.assertEqual(len(handlers), 0)


    def test_get_app_permissions(self):
        instance = PermissionHandler(model=Article)

        # get all permissions related to 'permission'
        app_permissions = Permission.objects.filter(
                content_type__app_label='permission'
            )
        app_permissions = set([u"permission.%s" % p.codename for p in app_permissions.all()])

        self.assertEqual(instance.get_app_permissions(), app_permissions)

    def test_get_model_permissions(self):
        instance = PermissionHandler(model=Article)

        # get all permissions related to Article
        model_permissions = Permission.objects.filter(
                content_type__app_label='permission',
                content_type__model='article'
            )
        model_permissions = set([u"permission.%s" % p.codename for p in model_permissions.all()])

        self.assertEqual(instance.get_model_permissions(), model_permissions)

    def test_get_permissions(self):
        class TestPermissionHandler(PermissionHandler):
            pass
        instance = TestPermissionHandler(model=Article)

        # get_permissions should return same value as
        # get_model_permissions in default
        self.assertEqual(
                instance.get_permissions(),
                instance.get_model_permissions()
            )

    def test_get_permissions_with_permissions(self):
        class TestPermissionHandler(PermissionHandler):
            permissions = (
                    'auth.add_user', 'auth.change_user', 'auth.delete_user'
                )
        instance = TestPermissionHandler(model=Article)

        # get_permissions should return the value specified
        self.assertEqual(
                instance.get_permissions(),
                set(['auth.add_user', 'auth.change_user', 'auth.delete_user'])
            )

    def test_get_permissions_with_get_permissions(self):
        class TestPermissionHandler(PermissionHandler):
            def get_permissions(self):
                return set([
                    'auth.add_user', 'auth.change_user', 'auth.delete_user'
                ])

        instance = TestPermissionHandler(model=Article)

        # get_permissions should return the value specified
        self.assertEqual(
                instance.get_permissions(),
                set(['auth.add_user', 'auth.change_user', 'auth.delete_user'])
            )

    def test_get_permission_codename(self):
        instance = PermissionHandler(model=Article)

        perm = 'app_label.name_model'
        codename = instance.get_permission_codename(perm)
        self.assertEqual(codename, 'name_model')

        perm = 'app_label.app_label.name_model'
        codename = instance.get_permission_codename(perm)
        self.assertEqual(codename, 'app_label.name_model')

        perm = 'name_model'
        codename = instance.get_permission_codename(perm)
        self.assertEqual(codename, 'name_model')

        perm = 'name'
        codename = instance.get_permission_codename(perm)
        self.assertEqual(codename, 'name')


    def test_has_perm_raise_exception(self):
        instance = PermissionHandler(model=Article)

        self.assertRaises(
                NotImplementedError,
                instance.has_perm,
                None, None, None
            )
