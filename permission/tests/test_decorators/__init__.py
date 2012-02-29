from __future__ import with_statement
from test_function_decorators import *
from test_method_decorators import *
from test_class_decorators import *

from django.test import TestCase
from django.http import HttpRequest
from django.views.generic import View

from permission.decorators import permission_required
from permission.decorators.class_decorators import permission_required as class_permission_required
from permission.decorators.method_decorators import permission_required as method_permission_required
from permission.decorators.function_decorators import permission_required as function_permission_required
from permission.tests.mock import MagicMock as Mock
from permission.tests.override_settings import with_apps

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
        from permission.tests.test_app.models import Article
        return Article.objects.get(pk=1)

class_permission_required = class_permission_required('test_app.add_article')
method_permission_required = method_permission_required('test_app.add_article')
function_permission_required = function_permission_required('test_app.add_article')

@with_apps('permission.tests.test_app')
class PermissionDecoratorsTestCase(TestCase):

    fixtures = ('permission_test_app.yaml',)

    def setUp(self):
        self.mock_request = Mock(spec=HttpRequest)
        self.mock_request.META = Mock()
        self.mock_request.user = Mock()
        self.mock_request.user.is_active.return_value = True
        self.mock_request.user.is_authenticated.return_value = True

    def test_function_views(self):
        from permission.tests.test_app.models import Article
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
        from permission.tests.test_app.models import Article
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
        from permission.tests.test_app.models import Article
        # class view of course can handle
        class_view = class_permission_required(ViewBase)
        class_view.as_view()(self.mock_request, pk=1)

        # method_decorators of course can handle
        method_view = method_permission_required(ViewBase)
        self.assertFalse(hasattr(method_view, 'as_view'))

        # function_decorators of course can handle
        function_view = function_permission_required(ViewBase)
        self.assertFalse(hasattr(method_view, 'as_view'))
