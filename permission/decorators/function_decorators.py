#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Generic view function decorators


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
import copy
import datetime
from functools import wraps
from django.http import Http404
from django.utils.decorators import available_attrs
from django.core.exceptions import PermissionDenied

from utils import redirect_to_login
from utils import get_object_from_date_based_view
from utils import get_object_from_list_detail_view

__all__ = ['permission_required']


def permission_required(perm, queryset=None, login_url=None, raise_exception=False):
    def wrapper(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def inner(request, *args, **kwargs):
            _kwargs = copy.copy(kwargs)
            # overwrite queryset if specified
            if queryset:
                _kwargs['queryset'] = queryset

            # get object from view
            if 'date_field' in _kwargs:
                fn = get_object_from_date_based_view
            else:
                fn = get_object_from_list_detail_view
            if fn.validate(request, *args, **_kwargs):
                obj = fn(request, *args, **_kwargs)
            else:
                # required arguments is not passed
                obj = None

            if not request.user.has_perm(perm, obj=obj):
                if raise_exception:
                    raise PermissionDenied
                else:
                    return redirect_to_login(request, login_url)
            return view_func(request, *args, **_kwargs)
        return inner
    return wrapper

