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

from permission.handlers import registry
from permission.handlers import PermissionHandler
from permission.backends import PermissionBackend
from permission.tests.models import Article

try:
    from django.test.utils import override_settings
except ImportError:
    from override_settings import override_settings

class TestPermissionHandler(PermissionHandler):
    called = False
    def has_perm(self, user_obj, perm, obj=None):
        self.called = True
        if not user_obj.is_authenticated():
            # No anonymous user have all permissions
            return False
        codename = self.get_permission_codename(perm)
        if codename == 'add_article':
            # Authenticated user have add permission
            return True
        if obj and obj.author == user_obj:
            # Author have change/delete permission
            return True
        # Others doesn't
        return False

class PermissionBackendTestCase(TestCase):

    fixtures = ('django_permission_test_datas.yaml',)

    def setUp(self):
        from django.contrib.auth.models import User
        from django.contrib.auth.models import AnonymousUser
        self.anonymous = AnonymousUser()
        # superuser
        self.user1 = User.objects.get(username='permission_test_user1')
        # staff
        self.user2 = User.objects.get(username='permission_test_user2')
        # normal
        self.user3 = User.objects.get(username='permission_test_user3')
        self.user4 = User.objects.get(username='permission_test_user4')
        # author = user3
        self.article1 = Article.objects.get(title='permission_test_article1')
        # author = user4
        self.article2 = Article.objects.get(title='permission_test_article2')

        # backup original registry
        self._original_registry = registry._registry
        registry._registry = {}

    def tearDown(self):
        # restore original registry
        registry._registry = self._original_registry

    def test_attributes_required(self):
        backend = PermissionBackend()

        self.assertTrue(hasattr(backend, 'supports_object_permissions'))
        self.assertTrue(getattr(backend, 'supports_object_permissions'))

        self.assertTrue(hasattr(backend, 'supports_anonymous_user'))
        self.assertTrue(getattr(backend, 'supports_anonymous_user'))

        self.assertTrue(hasattr(backend, 'supports_inactive_user'))
        self.assertTrue(getattr(backend, 'supports_inactive_user'))

        self.assertTrue(hasattr(backend, 'authenticate'))
        self.assertEqual(backend.authenticate(None, None), None)

        self.assertTrue(hasattr(backend, 'has_perm'))

    def test_has_perm(self):
        registry.register(Article, TestPermissionHandler)

        backend = PermissionBackend()

        # the registered handler is used
        backend.has_perm(self.anonymous, 'permission.add_article')
        self.assertTrue(registry._registry[Article].called)

        # the handler treat 'add', 'chage', 'delete' permissions
        permissions = registry._registry[Article].get_permissions()
        self.assertTrue('permission.add_article' in permissions)
        self.assertTrue('permission.change_article' in permissions)
        self.assertTrue('permission.delete_article' in permissions)

        # anonymous user have no permission
        self.assertFalse(backend.has_perm(self.anonymous, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.anonymous, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.anonymous, 'permission.delete_article', self.article1
            ))
        # superuser have all permission generally but in this backend, they 
        # don't. the permissions for superuser will handled by downstream.
        self.assertTrue(backend.has_perm(self.user1, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user1, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user1, 'permission.delete_article', self.article1
            ))
        # staff user
        self.assertTrue(backend.has_perm(self.user2, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user2, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user2, 'permission.delete_article', self.article1
            ))
        # user3 is an author of the article1 so have all permissions
        # but for article2
        self.assertTrue(backend.has_perm(self.user3, 'permission.add_article'))
        self.assertTrue(backend.has_perm(
                self.user3, 'permission.change_article', self.article1
            ))
        self.assertTrue(backend.has_perm(
                self.user3, 'permission.delete_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user3, 'permission.change_article', self.article2
            ))
        self.assertFalse(backend.has_perm(
                self.user3, 'permission.delete_article', self.article2
            ))
        # user4 is an author of the article2 so have all permissions
        # but for article1
        self.assertTrue(backend.has_perm(self.user4, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user4, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user4, 'permission.delete_article', self.article1
            ))
        self.assertTrue(backend.has_perm(
                self.user4, 'permission.change_article', self.article2
            ))
        self.assertTrue(backend.has_perm(
                self.user4, 'permission.delete_article', self.article2
            ))

    def test_has_perm_permissions(self):
        class TestPermissionHandler2(TestPermissionHandler):
            # 'permission.add_article' is removed so the handler is not used
            # for treating that permission.
            permissions = [
                'permission.change_article', 
                'permission.delete_article',
            ]
        registry.register(Article, TestPermissionHandler2)

        backend = PermissionBackend()

        # the handler treat 'chage', 'delete' permissions
        permissions = registry._registry[Article].get_permissions()
        self.assertFalse('permission.add_article' in permissions)
        self.assertTrue('permission.change_article' in permissions)
        self.assertTrue('permission.delete_article' in permissions)

        # anonymous user have no permission
        self.assertFalse(backend.has_perm(self.anonymous, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.anonymous, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.anonymous, 'permission.delete_article', self.article1
            ))
        # superuser have all permission generally but in this backend, they 
        # don't. the permissions for superuser will handled by downstream.
        self.assertFalse(backend.has_perm(self.user1, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user1, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user1, 'permission.delete_article', self.article1
            ))
        # staff user
        self.assertFalse(backend.has_perm(self.user2, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user2, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user2, 'permission.delete_article', self.article1
            ))
        # user3 is an author of the article1 so have all permissions
        # but for article2
        self.assertFalse(backend.has_perm(self.user3, 'permission.add_article'))
        self.assertTrue(backend.has_perm(
                self.user3, 'permission.change_article', self.article1
            ))
        self.assertTrue(backend.has_perm(
                self.user3, 'permission.delete_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user3, 'permission.change_article', self.article2
            ))
        self.assertFalse(backend.has_perm(
                self.user3, 'permission.delete_article', self.article2
            ))
        # user4 is an author of the article2 so have all permissions
        # but for article1
        self.assertFalse(backend.has_perm(self.user4, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user4, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user4, 'permission.delete_article', self.article1
            ))
        self.assertTrue(backend.has_perm(
                self.user4, 'permission.change_article', self.article2
            ))
        self.assertTrue(backend.has_perm(
                self.user4, 'permission.delete_article', self.article2
            ))

    def test_has_perm_get_permissions(self):
        class TestPermissionHandler2(TestPermissionHandler):
            # 'permission.add_article' is removed so the handler is not used
            # for treating that permission.
            def get_permissions(self):
                return set(['permission.change_article', 'permission.delete_article',])
        registry.register(Article, TestPermissionHandler2)

        backend = PermissionBackend()

        # the handler treat 'chage', 'delete' permissions
        permissions = registry._registry[Article].get_permissions()
        self.assertFalse('permission.add_article' in permissions)
        self.assertTrue('permission.change_article' in permissions)
        self.assertTrue('permission.delete_article' in permissions)

        # anonymous user have no permission
        self.assertFalse(backend.has_perm(self.anonymous, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.anonymous, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.anonymous, 'permission.delete_article', self.article1
            ))
        # superuser have all permission generally but in this backend, they 
        # don't. the permissions for superuser will handled by downstream.
        self.assertFalse(backend.has_perm(self.user1, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user1, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user1, 'permission.delete_article', self.article1
            ))
        # staff user
        self.assertFalse(backend.has_perm(self.user2, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user2, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user2, 'permission.delete_article', self.article1
            ))
        # user3 is an author of the article1 so have all permissions
        # but for article2
        self.assertFalse(backend.has_perm(self.user3, 'permission.add_article'))
        self.assertTrue(backend.has_perm(
                self.user3, 'permission.change_article', self.article1
            ))
        self.assertTrue(backend.has_perm(
                self.user3, 'permission.delete_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user3, 'permission.change_article', self.article2
            ))
        self.assertFalse(backend.has_perm(
                self.user3, 'permission.delete_article', self.article2
            ))
        # user4 is an author of the article2 so have all permissions
        # but for article1
        self.assertFalse(backend.has_perm(self.user4, 'permission.add_article'))
        self.assertFalse(backend.has_perm(
                self.user4, 'permission.change_article', self.article1
            ))
        self.assertFalse(backend.has_perm(
                self.user4, 'permission.delete_article', self.article1
            ))
        self.assertTrue(backend.has_perm(
                self.user4, 'permission.change_article', self.article2
            ))
        self.assertTrue(backend.has_perm(
                self.user4, 'permission.delete_article', self.article2
            ))

    def test_auth_backend(self):
        registry.register(Article, TestPermissionHandler)

        with override_settings(AUTHENTICATION_BACKENDS=(
                    'django.contrib.auth.backends.ModelBackend',
                    'permission.backends.PermissionBackend',
                )):

            # PermissionBackend is used
            def is_permission_backend_used():
                from django.contrib.auth import get_backends
                for backend in get_backends():
                    if isinstance(backend, PermissionBackend):
                        return True
                return False
            self.assertTrue(is_permission_backend_used())

            # the handler treat 'add', 'chage', 'delete' permissions
            permissions = registry._registry[Article].get_permissions()
            self.assertTrue('permission.add_article' in permissions)
            self.assertTrue('permission.change_article' in permissions)
            self.assertTrue('permission.delete_article' in permissions)

            # the registered handler is used (user1 is superuser so cannot be
            # used for this)
            self.user2.has_perm('permission.add_article')
            self.assertTrue(registry._registry[Article].called)

            # superuser have all permission with ModelBackend
            self.assertTrue(self.user1.has_perm('permission.add_article'))
            self.assertTrue(self.user1.has_perm(
                    'permission.change_article', self.article1
                ))
            self.assertTrue(self.user1.has_perm(
                    'permission.delete_article', self.article1
                ))
            # staff
            self.assertTrue(self.user2.has_perm('permission.add_article'))
            self.assertFalse(self.user2.has_perm(
                    'permission.change_article', self.article1
                ))
            self.assertFalse(self.user2.has_perm(
                    'permission.delete_article', self.article1
                ))
            # user3 have all permissions for article1 but article2
            self.assertTrue(self.user3.has_perm('permission.add_article'))
            self.assertTrue(self.user3.has_perm(
                    'permission.change_article', self.article1
                ))
            self.assertTrue(self.user3.has_perm(
                    'permission.delete_article', self.article1
                ))
            self.assertFalse(self.user3.has_perm(
                    'permission.change_article', self.article2
                ))
            self.assertFalse(self.user3.has_perm(
                    'permission.delete_article', self.article2
                ))
            # user4 have all permissions for article2 but article1
            self.assertTrue(self.user4.has_perm('permission.add_article'))
            self.assertFalse(self.user4.has_perm(
                    'permission.change_article', self.article1
                ))
            self.assertFalse(self.user4.has_perm(
                    'permission.delete_article', self.article1
                ))
            self.assertTrue(self.user4.has_perm(
                    'permission.change_article', self.article2
                ))
            self.assertTrue(self.user4.has_perm(
                    'permission.delete_article', self.article2
                ))

        # without AUTH backend, handler wount called
        with override_settings(AUTHENTICATION_BACKENDS=(
                    'django.contrib.auth.backends.ModelBackend',
                )):

            # PermissionBackend is not used
            def is_permission_backend_used():
                from django.contrib.auth import get_backends
                for backend in get_backends():
                    if isinstance(backend, PermissionBackend):
                        return True
                return False
            self.assertFalse(is_permission_backend_used())

            # superuser have all permission with ModelBackend
            self.assertTrue(self.user1.has_perm('permission.add_article'))
            self.assertTrue(self.user1.has_perm(
                    'permission.change_article', self.article1
                ))
            self.assertTrue(self.user1.has_perm(
                    'permission.delete_article', self.article1
                ))
            # users have no permissions
            self.assertFalse(self.user2.has_perm('permission.add_article'))
            self.assertFalse(self.user2.has_perm(
                    'permission.change_article', self.article1
                ))
            self.assertFalse(self.user2.has_perm(
                    'permission.delete_article', self.article1
                ))
            self.assertFalse(self.user3.has_perm('permission.add_article'))
            self.assertFalse(self.user3.has_perm(
                    'permission.change_article', self.article1
                ))
            self.assertFalse(self.user3.has_perm(
                    'permission.delete_article', self.article1
                ))
            self.assertFalse(self.user3.has_perm(
                    'permission.change_article', self.article2
                ))
            self.assertFalse(self.user3.has_perm(
                    'permission.delete_article', self.article2
                ))
            self.assertFalse(self.user4.has_perm('permission.add_article'))
            self.assertFalse(self.user4.has_perm(
                    'permission.change_article', self.article1
                ))
            self.assertFalse(self.user4.has_perm(
                    'permission.delete_article', self.article1
                ))
            self.assertFalse(self.user4.has_perm(
                    'permission.change_article', self.article2
                ))
            self.assertFalse(self.user4.has_perm(
                    'permission.delete_article', self.article2
                ))
