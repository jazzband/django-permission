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
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

from permission.tests.utils import mock_request
from permission.tests.models import Article

def prepare_with_anonymous_user():
    request = mock_request()
    setattr(request, 'user',  AnonymousUser())
    queryset = Article.objects.all()
    args = ()
    kwargs = {
            'object_id': 1,
            'slug': 'permission_test_article1',
            'slug_field': 'title',
            'date_field': 'created_at',
            'year': 2000,
            'month': 1,
            'day': 1,
            'month_format': '%%m',
            'day_format': '%%d',
        }
    return request, queryset, args, kwargs

def prepare_with_authenticated_user():
    request, queryset, args, kwargs = prepare_with_anonymous_user()
    request.user = User.objects.get(username='permission_test_user1')
    return request, queryset, args, kwargs
