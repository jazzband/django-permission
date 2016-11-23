from django.test import TestCase
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
from ...utils.handlers import registry
from ...decorators.functionbase import permission_required as f
from ...decorators.methodbase import permission_required as m
from ...decorators.classbase import permission_required as c
from ...decorators import permission_required as p
from ..compat import MagicMock
from .utils import (
    create_mock_handler,
    create_mock_request,
    create_mock_queryset,
    create_mock_model,
    create_mock_view_func,
    create_mock_view_class,
)

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
    # Classbased generic view related test will not be run so never mind.
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
        # restore original registry
        registry._registry = self._original_registry

    def test_function_views(self):

        # class decorator cannot handle
        self.assertRaises(AttributeError, c, view_func)
        # method decorator can handle
        method_view = m(view_func)
        method_view(self.request, self.queryset, object_id=1)

        # function decorator can handle
        function_view = f(view_func)
        function_view(self.request, self.queryset, object_id=1)

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
