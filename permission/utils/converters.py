# vim: set fileencoding=utf-8 :
"""
Utilities of handling django permission


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
from django.contrib.auth.models import Permission


def perm_to_permission(perm):
    """
    Convert string permission to permission instance.
    The string permission must be written as
    ``"app_label.codename"``

    Usage::

        >>> permission = perm_to_permission('auth.add_user')
        >>> permission.content_type.app_label
        u'auth'
        >>> permission.codename
        u'add_user'

    """
    try:
        app_label, codename = perm.split('.', 1)
    except IndexError:
        raise AttributeError(
                "passed string perm has wrong format. "
                "string perm should be 'app_label.codename'."
            )
    else:
        permission = Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename
            )
        return permission

def permission_to_perm(permission):
    """
    Convert permission instance to string permission.

    Usage::

        >>> permission = Permission.objects.get(
        ...     content_type__app_label='auth',
        ...     codename='add_user',
        ... )
        >>> permission_to_perm(permission)
        u'auth.add_user'

    """
    app_label = permission.content_type.app_label
    codename = permission.codename
    return "%s.%s" % (app_label, codename)

