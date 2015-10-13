# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.core.exceptions import PermissionDenied
from permission.utils.handlers import registry
from permission.tests.test_decorators.utils import create_mock_handler
from permission.tests.test_decorators.utils import create_mock_request
from permission.tests.test_decorators.utils import create_mock_view_func
from permission.tests.test_decorators.utils import create_mock_queryset
from permission.tests.test_decorators.utils import create_mock_model
from permission.decorators.functionbase import permission_required


class PermissionFunctionDecoratorsTestCase(TestCase):
    def setUp(self):
        self.handler = create_mock_handler()
        self.request = create_mock_request(self.handler)
        self.model = create_mock_model()
        self.model_instance = self.model()
        self.queryset = create_mock_queryset(self.model_instance)
        self.view_func = create_mock_view_func()
        self.decorated = permission_required(
                'permission.add_article')(self.view_func)
        self.decorated_exc = permission_required(
                'permission.add_article', raise_exception=True)(self.view_func)

        # store original registry
        self._original_registry = registry._registry

        # clear registry and register mock handler
        registry._registry = {}
        registry.register(
                self.model,
                self.handler,
            )

    def tearDown(self):
        # restore original reigstry
        registry._registry = self._original_registry


    def test_list_detail_object_id(self):
        # has_perm always return False
        self.view_func.called = False
        self.handler.has_perm.return_value = False
        self.decorated(self.request, 
                       queryset=self.queryset,
                       object_id=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertFalse(self.view_func.called)

        self.assertRaises(PermissionDenied, self.decorated_exc,
                          self.request, queryset=self.queryset,
                          object_id=1)
        self.assertFalse(self.view_func.called)

        # has_perm always return True
        self.handler.has_perm.return_value = True
        self.decorated(
                self.request, 
                queryset=self.queryset,
                object_id=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertTrue(self.view_func.called)

    def test_list_detail_slug(self):
        self.view_func.called = False
        self.handler.has_perm.return_value = False
        # has_perm always return False
        self.decorated(
                self.request, 
                queryset=self.queryset, 
                slug='permission_test_article1',
                slug_field='title')
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertFalse(self.view_func.called)
        # has_perm always return True
        self.handler.has_perm.return_value = True
        self.decorated(
                self.request, 
                queryset=self.queryset, 
                slug='permission_test_article1',
                slug_field='title')
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertTrue(self.view_func.called)

    def test_date_based_object_id(self):
        self.view_func.called = False
        self.handler.has_perm.return_value = False
        # has_perm always return False
        self.decorated(
                self.request, 
                queryset=self.queryset, 
                year='2000', month='1', day='1',
                date_field='created_at',
                month_format='%m',
                object_id=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertFalse(self.view_func.called)
        # has_perm always return True
        self.handler.has_perm.return_value = True
        self.decorated(
                self.request, 
                queryset=self.queryset,
                year='2000', month='1', day='1',
                date_field='created_at',
                month_format='%m',
                object_id=1)
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertTrue(self.view_func.called)

    def test_date_based_slug(self):
        self.view_func.called = False
        self.handler.has_perm.return_value = False
        # has_perm always return False
        self.decorated(
                self.request, 
                queryset=self.queryset, 
                year='2000', month='1', day='1',
                date_field='created_at',
                month_format='%m',
                slug='permission_test_article1',
                slug_field='title')
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertFalse(self.view_func.called)
        # has_perm always return True
        self.handler.has_perm.return_value = True
        self.decorated(
                self.request, 
                queryset=self.queryset, 
                year='2000', month='1', day='1',
                date_field='created_at',
                month_format='%m',
                slug='permission_test_article1',
                slug_field='title')
        self.request.user.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.handler.has_perm.assert_called_with(
                'permission.add_article',
                obj=self.model_instance,
            )
        self.assertTrue(self.view_func.called)

