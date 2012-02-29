#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Classbased generic view method decorator which also can handle
functional generic view.


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
from functools import wraps
from django.http import HttpRequest
from django.utils.decorators import available_attrs

from utils import redirect_to_login
from utils import get_object_from_classbased_instance
from function_decorators import permission_required as function_permission_required

__all__ = ['permission_required']

def permission_required(perm, queryset=None, login_url=None, raise_exception=False):
    def wrapper(view_method):                
        @wraps(view_method, assigned=available_attrs(view_method))
        def inner(self, request=None, *args, **kwargs):
            if isinstance(self, HttpRequest):
                # this is a functional view not classbased view.
                decorator = function_permission_required(perm, queryset, login_url, raise_exception)
                decorator = decorator(view_method)
                if not request:
                    args = list(args)
                    args.insert(0, request)
                request = self
                return decorator(request, *args, **kwargs)
            else:
                # get object
                obj = get_object_from_classbased_instance(
                        self, queryset, request, *args, **kwargs
                    )
                
                if not request.user.has_perm(perm, obj=obj):
                    return redirect_to_login(request, login_url, raise_exception)
                return view_method(self, request, *args, **kwargs)
        return inner
    return wrapper
