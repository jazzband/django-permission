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
from django.http import HttpResponse

from permission import registry
from permission.decorators.function_decorators import permission_required
from permission.tests.mock import MagicMock as Mock
from permission.tests.override_settings import with_apps

@with_apps('permission.tests.test_app')
class PermissionFunctionDecoratorsTestCase(TestCase):

    fixtures = ('permission_test_app.yaml',)

    def setUp(self):
        from permission.tests.test_app.models import Article
        mock_handler = Mock(**{
                'has_perm.return_value': False,
                'get_permissions.return_value': 'test_app.add_article',
            })
        mock_request = Mock()
        mock_request.META = Mock()
        mock_request.user = Mock()
        mock_request.user.is_active.return_value = True
        mock_request.user.is_authenticated.return_value = True
        mock_request.user.has_perm.side_effect = mock_handler.has_perm

        self.mock_handler = mock_handler
        self.mock_request = mock_request

        # clear registry and register mock handler
        registry._registry = {}
        registry._permissions = {}
        registry.register(
                Article,
                Mock(return_value=self.mock_handler)
            )
        self.view_func = Mock(return_value=HttpResponse())
        self.decorated = permission_required('test_app.add_article')(self.view_func)


    def test_list_detail_object_id(self):
        from permission.tests.test_app.models import Article
        self.assertEqual(registry._registry[Article], self.mock_handler)

        # has_perm always return False
        self.decorated(
                self.mock_request, 
                queryset=Article.objects.all(), 
                object_id=1)
        self.mock_request.user.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.mock_handler.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.assertFalse(self.view_func.called)
        # has_perm always return True
        self.mock_handler.has_perm.return_value = True
        self.decorated(
                self.mock_request, 
                queryset=Article.objects.all(), 
                object_id=1)
        self.mock_request.user.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.mock_handler.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.assertTrue(self.view_func.called)

    def test_list_detail_slug(self):
        from permission.tests.test_app.models import Article
        self.assertEqual(registry._registry[Article], self.mock_handler)

        # has_perm always return False
        self.decorated(
                self.mock_request, 
                queryset=Article.objects.all(), 
                slug='permission_test_article1',
                slug_field='title')
        self.mock_request.user.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.mock_handler.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.assertFalse(self.view_func.called)
        # has_perm always return True
        self.mock_handler.has_perm.return_value = True
        self.decorated(
                self.mock_request, 
                queryset=Article.objects.all(), 
                slug='permission_test_article1',
                slug_field='title')
        self.mock_request.user.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.mock_handler.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.assertTrue(self.view_func.called)

    def test_date_based_object_id(self):
        from permission.tests.test_app.models import Article
        self.assertEqual(registry._registry[Article], self.mock_handler)

        # has_perm always return False
        self.decorated(
                self.mock_request, 
                queryset=Article.objects.all(), 
                year='2000', month='1', day='1',
                date_field='created_at',
                month_format='%m',
                object_id=1)
        self.mock_request.user.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.mock_handler.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.assertFalse(self.view_func.called)
        # has_perm always return True
        self.mock_handler.has_perm.return_value = True
        self.decorated(
                self.mock_request, 
                queryset=Article.objects.all(), 
                year='2000', month='1', day='1',
                date_field='created_at',
                month_format='%m',
                object_id=1)
        self.mock_request.user.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.mock_handler.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.assertTrue(self.view_func.called)

    def test_date_based_slug(self):
        from permission.tests.test_app.models import Article
        self.assertEqual(registry._registry[Article], self.mock_handler)

        # has_perm always return False
        self.decorated(
                self.mock_request, 
                queryset=Article.objects.all(), 
                year='2000', month='1', day='1',
                date_field='created_at',
                month_format='%m',
                slug='permission_test_article1',
                slug_field='title')
        self.mock_request.user.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.mock_handler.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.assertFalse(self.view_func.called)
        # has_perm always return True
        self.mock_handler.has_perm.return_value = True
        self.decorated(
                self.mock_request, 
                queryset=Article.objects.all(), 
                year='2000', month='1', day='1',
                date_field='created_at',
                month_format='%m',
                slug='permission_test_article1',
                slug_field='title')
        self.mock_request.user.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.mock_handler.has_perm.assert_called_with(
                'test_app.add_article',
                obj=Article.objects.get(pk=1)
            )
        self.assertTrue(self.view_func.called)

