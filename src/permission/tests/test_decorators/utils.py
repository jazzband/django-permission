# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db.models import Model
from django.http import HttpRequest
from django.http import HttpResponse
from permission.handlers import PermissionHandler
from permission.tests.compatibility import MagicMock


def create_mock_class(name, base, instance=None):
    instance = instance or MagicMock()
    mock_class = MagicMock(name=name,
                           return_value=instance)
    mock_class.__bases__ = (type, base)
    mock_class.__class__ = type
    return mock_class

def create_mock_handler():
    instance = MagicMock(**{
            'has_perm.return_value': False,
            'get_permissions.return_value': [
                'permission.add_article',
            ],
        })
    handler = create_mock_class('MockPermissionHandler',
                                base=PermissionHandler,
                                instance=instance)
    return handler


def create_mock_request(mock_permission_handler):
    request = MagicMock(spec=HttpRequest)
    request.build_absolute_uri = MagicMock(return_value="/")
    request.META = MagicMock()
    request.user = MagicMock(**{
            'is_active.return_value': True,
            'is_authenticated.return_value': True,
            'has_perm.side_effect': mock_permission_handler.has_perm,
        })
    return request


def create_mock_view_func():
    response = MagicMock(spec=HttpResponse)
    function = MagicMock(return_value=response)
    return function


def create_mock_view_class(view_func):
    from django.views.generic import View
    view_class = type('MockView', (View,), {})
    view_class.dispatch = view_func
    return view_class


def create_mock_model():
    instance = MagicMock()
    model = MagicMock(name='MockModel')
    model.__bases__ = (type,)
    model.__class__ = type
    model._meta = MagicMock(**{
            'abstract': False,
        })
    return model


def create_mock_queryset(obj):
    from django.db.models.query import QuerySet
    from django.core.exceptions import ObjectDoesNotExist
    def get_side_effect(*args, **kwargs):
        if kwargs.get('pk', None) == 1:
            return obj
        if kwargs.get('title', None) == 'permission_test_article1':
            return obj
        if kwargs.get('title__exact', None) == 'permission_test_article1':
            return obj
        raise queryset.model.DoesNotEixst
    queryset = MagicMock(spec=QuerySet, **{
            'get.side_effect': get_side_effect,
        })
    queryset.model = MagicMock()
    queryset.model.DoesNotEixst = ObjectDoesNotExist
    queryset.model._meta = MagicMock(object_name='MockQuerysetModel')
    return queryset
