#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Utils used in decorators


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
import time
import datetime
import urlparse
from django.conf import settings
from django.http import Http404
from django.db.models.fields import DateTimeField
from django.shortcuts import get_object_or_404
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic.edit import BaseCreateView
from permission.exceptions import ValidationError

try:
    from django.utils import timezone
    datetime_now = timezone.now
except ImportError:
    datetime_now = datetime.datetime.now

def redirect_to_login(request, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """redirect to login"""
    path = request.build_absolute_uri()
    # if the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse.urlparse(login_url or settings.LOGIN_URL)[:2]
    current_scheme, current_netloc = urlparse.urlparse(path)[:2]
    if ((not login_scheme or login_scheme == current_scheme) and
        (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()
    from django.contrib.auth.views import redirect_to_login as auth_redirect_to_login
    return auth_redirect_to_login(path, login_url, redirect_field_name)

def get_object_from_classbased_instance(instance, queryset, request, *args, **kwargs):
    """get object from an instance of classbased generic view"""
    # initialize request, args, kwargs of classbased_instance
    # most of methods of classbased view assumed these attributes
    # but these attributes is initialized in ``dispatch`` method.
    instance.request = request
    instance.args = args
    instance.kwargs = kwargs

    # get queryset from class if ``queryset_or_model`` is not specified
    if hasattr(instance, 'get_queryset') and not queryset:
        queryset = instance.get_queryset()
    elif hasattr(instance, 'queryset') and not queryset:
        queryset = instance.queryset
    elif hasattr(instance, 'model') and not queryset:
        queryset = instance.model._default_manager.all()
        
    # get object
    if hasattr(instance, 'get_object'):
        try:
            obj = instance.get_object(queryset)
        except AttributeError, e:
            # CreateView has ``get_object`` method but CreateView
            # should not have any object before thus simply set
            # None
            if isinstance(instance, BaseCreateView):
                obj = None
            else:
                raise e
    elif hasattr(instance, 'object'):
        obj = instance.object
    else:
        obj = None
    return obj

def get_object_from_list_detail_view(request, *args, **kwargs):
    """get object from generic list_detail.detail view"""
    queryset = kwargs['queryset']
    object_id = kwargs.get('object_id', None)
    slug = kwargs.get('slug', None)
    slug_field = kwargs.get('slug_field', 'slug')
    if object_id:
        obj = get_object_or_404(queryset, pk=object_id)
    elif slug and slug_field:
        obj = get_object_or_404(queryset, **{slug_field: slug})
    else:
        raise AttributeError(
                "Generic detail view must be called with either an "
                "object_id or a slug/slug_field."
            )
    return obj
def _get_object_from_list_detail_view_validation(request, *args, **kwargs):
    if 'queryset' not in kwargs:
        return False
    elif 'object_id' not in kwargs and 'slug' not in kwargs:
        return False
    return True
get_object_from_list_detail_view.validate = _get_object_from_list_detail_view_validation


def get_object_from_date_based_view(request, *args, **kwargs):
    """get object from generic date_based.detail view"""
    year, month, day = kwargs['year'], kwargs['month'], kwargs['day']
    month_format = kwargs.get('month_format', '%b')
    day_format = kwargs.get('day_format', '%d')
    date_field = kwargs['date_field']
    queryset = kwargs['queryset']
    object_id = kwargs.get('object_id', None)
    slug = kwargs.get('slug', None)
    slug_field = kwargs.get('slug_field', 'slug')
    
    try:
        tt = time.strptime(
                '%s-%s-%s' % (year, month, day),
                '%s-%s-%s' % ('%Y', month_format, day_format)
            )
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    model = queryset.model

    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {
                '%s__range' % date_field: (
                    datetime.datetime.combine(date, datetime.time.min),
                    datetime.datetime.combine(date, datetime.time.max),
                )}
    else:
        lookup_kwargs = {date_field: date}

    now = datetime_now()
    if date >= now.date() and not kwargs.get('allow_future', False):
        lookup_kwargs['%s__lte' % date_field] = now
    if object_id:
        lookup_kwargs['pk'] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        raise AttributeError(
                "Generic detail view must be called with either an "
                "object_id or a slug/slug_field."
            )
    return get_object_or_404(queryset, **lookup_kwargs)
def _get_object_from_date_based_view_validation(request, *args, **kwargs):
    if 'queryset' not in kwargs:
        return False
    elif 'year' not in kwargs or 'month' not in kwargs or 'day' not in kwargs:
        return False
    elif 'object_id' not in kwargs and 'slug' not in kwargs:
        return False
    return True
get_object_from_date_based_view.validate = _get_object_from_date_based_view_validation
