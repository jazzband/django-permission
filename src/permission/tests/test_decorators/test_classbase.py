# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import django
from django.test import TestCase
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
from permission.decorators.classbase import permission_required


@skipIf(
    django.VERSION < (1, 3),
    'Classbase generic view is not supported int his version')
class PermissionClassDecoratorsTestCase(TestCase):
    def setUp(self):
        self.handler = create_mock_handler()
        self.request = create_mock_request(self.handler)
        self.model = create_mock_model()
        self.model_instance = self.model()
        self.queryset = create_mock_queryset(self.model_instance)

        self.view_func = create_mock_view_func()
        self.view_class = permission_required(
                'permission.add_article')(
                    create_mock_view_class(self.view_func)
                )
        self.view_class_exc = permission_required(
                'permission.add_article',
                raise_exception=True)(
                    create_mock_view_class(self.view_func)
                )

        # store original registry
        self._original_registry = registry._registry

        # clear registry and register mock handler
        registry._registry = {}
        registry.register(
                self.model,
                self.handler,
            )

        # clear call history
        self.handler.has_perm.return_value = False

    def tearDown(self):
        # restore original reigstry
        registry._registry = self._original_registry


    def test_with_object(self):
        # set object
        self.view_class.object = self.model_instance
        self.view_class_exc.object = self.model_instance

        # has_perm always return False
        self.view_class.as_view()(self.request, pk=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertFalse(self.view_func.called)

        self.assertRaises(PermissionDenied,
                          self.view_class_exc.as_view(),
                          self.request, 
                          pk=1)
        self.assertFalse(self.view_func.called)

        # has_perm always return True
        self.handler.has_perm.return_value = True
        self.view_class.as_view()(self.request, pk=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertTrue(self.view_func.called)

    def test_with_get_object(self):
        # set object
        self.view_class.get_object = MagicMock(
                return_value=self.model_instance)
        self.view_class_exc.get_object = MagicMock(
                return_value=self.model_instance)

        # has_perm always return False
        self.view_class.as_view()(self.request, pk=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertFalse(self.view_func.called)

        self.assertRaises(PermissionDenied,
                          self.view_class_exc.as_view(),
                          self.request, 
                          pk=1)
        self.assertFalse(self.view_func.called)

        # has_perm always return True
        self.handler.has_perm.return_value = True
        self.view_class.as_view()(self.request, pk=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertTrue(self.view_func.called)

    def test_with_queryset(self):
        # set object
        get_object = lambda x, y: y.get(*x.args, **x.kwargs)
        self.view_class.get_object = get_object
        self.view_class_exc.get_object = get_object
        self.view_class.queryset = self.queryset
        self.view_class_exc.queryset = self.queryset

        # has_perm always return False
        self.view_class.as_view()(self.request, pk=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertFalse(self.view_func.called)

        self.assertRaises(PermissionDenied,
                          self.view_class_exc.as_view(),
                          self.request, 
                          pk=1)
        self.assertFalse(self.view_func.called)

        # has_perm always return True
        self.handler.has_perm.return_value = True
        self.view_class.as_view()(self.request, pk=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertTrue(self.view_func.called)

    def test_with_get_queryset(self):
        # set object
        get_object = lambda x, y: y.get(*x.args, **x.kwargs)
        self.view_class.get_object = get_object
        self.view_class_exc.get_object = get_object
        self.view_class.get_queryset = MagicMock(
                return_value=self.queryset)
        self.view_class_exc.get_queryset = MagicMock(
                return_value=self.queryset)

        # has_perm always return False
        self.view_class.as_view()(self.request, pk=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertFalse(self.view_func.called)

        self.assertRaises(PermissionDenied,
                          self.view_class_exc.as_view(),
                          self.request, 
                          pk=1)
        self.assertFalse(self.view_func.called)

        # has_perm always return True
        self.handler.has_perm.return_value = True
        self.view_class.as_view()(self.request, pk=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertTrue(self.view_func.called)

