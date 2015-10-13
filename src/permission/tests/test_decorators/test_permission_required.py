# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import django
from django.test import TestCase
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
from permission.utils.handlers import registry
from permission.tests.compatibility import skipIf
from permission.tests.compatibility import MagicMock
from permission.tests.test_decorators.utils import create_mock_handler
from permission.tests.test_decorators.utils import create_mock_request
from permission.tests.test_decorators.utils import create_mock_queryset
from permission.tests.test_decorators.utils import create_mock_model
from permission.tests.test_decorators.utils import create_mock_view_func
from permission.tests.test_decorators.utils import create_mock_view_class

from permission.decorators.functionbase import permission_required as f
from permission.decorators.methodbase import permission_required as m
from permission.decorators.classbase import permission_required as c
from permission.decorators import permission_required as p

p = p('permission.add_article')
c = c('permission.add_article')
m = m('permission.add_article')
f = f('permission.add_article')

model = create_mock_model()
instance = model()

def view_func(request, *args, **kwargs):
    assert isinstance(request, HttpRequest)
try:
    from django.views.generic import View as BaseView
except ImportError:
    # classbase generic view related test will not be run so never mind.
    BaseView = object

class View(BaseView):
    def dispatch(self, request, *args, **kwargs):
        assert isinstance(self, View)
        assert isinstance(request, HttpRequest)
    def get_object(self, queryset=None):
        return instance

class PermissionDecoratorsTestCase(TestCase):

    def setUp(self):
        self.handler = create_mock_handler()
        self.request = create_mock_request(self.handler)
        self.queryset = create_mock_queryset(instance)

        # store original registry
        self._original_registry = registry._registry

        # clear registry and register mock handler
        registry._registry = {}
        registry.register(
                model,
                self.handler,
            )

    def tearDown(self):
        # restore original reigstry
        registry._registry = self._original_registry

    def test_function_views(self):

        if django.VERSION >= (1, 3):
            # class decorator cannot handle
            self.assertRaises(AttributeError, c, view_func)
            # method decorator can handle
            method_view = m(view_func)
            method_view(self.request, self.queryset, object_id=1)

        # function decorator can handle
        function_view = f(view_func)
        function_view(self.request, self.queryset, object_id=1)

    @skipIf(
        django.VERSION < (1, 3),
        'Classbase generic view is not supported int his version')
    def test_method_views(self):
        view_method = View.dispatch

        # class decorator cannot handle
        self.assertRaises(AttributeError, c, View.dispatch)

        # method decorator can handle
        method_view = m(View.dispatch)
        method_view(View(), self.request, pk=1)

        # function decorators cannot handle
        function_view = f(View.dispatch)
        self.assertRaises(AttributeError, function_view,
                          View(), self.request, pk=1)

    @skipIf(
        django.VERSION < (1, 3),
        'Classbase generic view is not supported int his version')
    def test_class_views(self):
        # class decorator can handle
        class_view = c(View)
        class_view.as_view()(self.request, pk=1)

        # method decorator cannot handle
        method_view = m(View)
        self.assertFalse(hasattr(method_view, 'as_view'))

        # function decorator cannot handle
        function_view = f(View)
        self.assertFalse(hasattr(method_view, 'as_view'))

    @skipIf(
        django.VERSION < (1, 3),
        'Classbase generic view is not supported int his version')
    def test_permission_required(self):
        # function
        functional_view = p(view_func)
        functional_view(self.request, queryset=self.queryset, object_id=1)

        # method
        method_view = p(View.dispatch)
        method_view(View(), self.request, pk=1)

        # class
        class_view = p(View)
        class_view.as_view()(self.request, pk=1)
