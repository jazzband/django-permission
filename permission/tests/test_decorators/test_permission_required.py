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
from mock import MagicMock as Mock
from django.test import TestCase
from django.http import HttpRequest
from django.views.generic import View

from permission.decorators import permission_required
from permission.decorators import class_decorators 
from permission.decorators import method_decorators 
from permission.decorators import function_decorators 
from permission.tests.models import Article

def viewbase(request, *args, **kwargs):
    assert isinstance(request, HttpRequest), \
        'An instance of "HttpRequest" is expected but "%s" is passed' % request

class ViewBase(View):
    def dispatch(self, request, *args, **kwargs):
        assert isinstance(self, ViewBase), \
            'An instance of "ViewBase" is expected but "%s" is passed' % self
        assert isinstance(request, HttpRequest), \
            'An instance of "HttpRequest" is expected but "%s" is passed' % request
    def get_object(self, queryset=None):
        return Article.objects.get(pk=1)

permission_required = permission_required('permission.add_article')
class_permission_required = class_decorators.permission_required('permission.add_article')
method_permission_required = method_decorators.permission_required('permission.add_article')
function_permission_required = function_decorators.permission_required('permission.add_article')

class PermissionDecoratorsTestCase(TestCase):

    fixtures = ('django_permission_test_datas.yaml',)

    def setUp(self):
        self.mock_request = Mock(spec=HttpRequest)
        self.mock_request.META = Mock()
        self.mock_request.user = Mock()
        self.mock_request.user.is_active.return_value = True
        self.mock_request.user.is_authenticated.return_value = True

    def test_function_views(self):
        # class_decorators cannot handle
        self.assertRaises(
                AttributeError,
                class_permission_required,
                viewbase
            )
        # method_decorators can handle function as well
        method_view = method_permission_required(viewbase)
        method_view(
                self.mock_request, 
                queryset=Article.objects.all(),
                object_id=1,
            )

        # function_decorators of course can handle
        function_view = function_permission_required(viewbase)
        function_view(
                self.mock_request, 
                queryset=Article.objects.all(),
                object_id=1,
            )

    def test_method_views(self):
        # class_decorators cannot handle
        self.assertRaises(
                AttributeError,
                class_permission_required,
                ViewBase.dispatch
            )
        # method_decorators of course can handle
        method_view = method_permission_required(ViewBase.dispatch)
        method_view(ViewBase(), self.mock_request, pk=1)

        # function_decorators cannot handle
        function_view = function_permission_required(ViewBase.dispatch)
        self.assertRaises(
                AttributeError, function_view,
                ViewBase(), self.mock_request, pk=1,
            )

    def test_class_views(self):
        # class view of course can handle
        class_view = class_permission_required(ViewBase)
        class_view.as_view()(self.mock_request, pk=1)

        # method_decorators cannot handle
        method_view = method_permission_required(ViewBase)
        self.assertFalse(hasattr(method_view, 'as_view'))

        # function_decorators cannot handle
        function_view = function_permission_required(ViewBase)
        self.assertFalse(hasattr(method_view, 'as_view'))

    def test_permission_required(self):
        # function
        functional_view = permission_required(viewbase)
        functional_view(
                self.mock_request, 
                queryset=Article.objects.all(),
                object_id=1,
            )

        # method
        method_view = permission_required(ViewBase.dispatch)
        method_view(ViewBase(), self.mock_request, pk=1)

        # class
        class_view = permission_required(ViewBase)
        class_view.as_view()(self.mock_request, pk=1)
