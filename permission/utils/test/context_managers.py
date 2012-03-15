# vim: set fileencoding=utf-8 :
"""
Context managers


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
from permission.utils.converters import permission_to_perm
from permission.utils.converters import perm_to_permission


class permissions(object):
    """
    Context manager for adding extra user permissions
    to the ``user_obj`` instance. This doesn't add extra
    permissions on db.

    Usage::

        # Create user for testing
        >>> from django.contrib.auth.models import User
        >>> james = User.objects.create_user(
        ...     username='permission_test_user_james1',
        ...     email='permission_test_user_james1@test.com',
        ...     password='password',
        ... )
        >>> alice = User.objects.create_user(
        ...     username='permission_test_user_alice1',
        ...     email='permission_test_user_alice1@test.com',
        ...     password='password',
        ... )

        # They does not have 'auth.add_user' and 'auth.change_usr' permission
        >>> assert not james.has_perm('auth.add_user')
        >>> assert not alice.has_perm('auth.add_user')
        >>> assert not james.has_perm('auth.change_user')
        >>> assert not alice.has_perm('auth.change_user')

        # james have the permissions
        >>> with permissions(james, 'auth.add_user', 'auth.change_user'):
        ...     assert james.has_perm('auth.add_user')
        ...     assert not alice.has_perm('auth.add_user')
        ...     assert james.has_perm('auth.change_user')
        ...     assert not alice.has_perm('auth.change_user')
        ...     # But actually james doesn't have permission in db
        ...     assert not james.user_permissions.filter(
        ...             content_type__app_label='auth',
        ...             codename='add_user',
        ...         ).exists()

        # They does not have 'auth.add_user' and 'auth.change_usr' permission
        >>> assert not james.has_perm('auth.add_user')
        >>> assert not alice.has_perm('auth.add_user')
        >>> assert not james.has_perm('auth.change_user')
        >>> assert not alice.has_perm('auth.change_user')


    """
    def __init__(self, user_obj, *perms):
        self.user_obj = user_obj
        self.perms = perms
        # convert permission instance if necessary
        def convert_if_required(perm):
            if isinstance(perm, Permission):
                perm = permission_to_perm(perm)
            return perm
        self.perms = set([convert_if_required(p) for p in self.perms])
        self.original_get_all_permissions = self.user_obj.get_all_permissions

    def __enter__(self):
        def get_all_permissions(obj=None):
            perms = self.original_get_all_permissions(obj)
            perms = list(perms)
            perms.extend(self.perms)
            return set(perms)
        self.user_obj.get_all_permissions = get_all_permissions
        self.user_obj._perm_cache = get_all_permissions()
        return self.user_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        # restore original get_all_permissions method
        self.user_obj.get_all_permissions = self.original_get_all_permissions
        delattr(self.user_obj, '_perm_cache')

class real_permissions(object):
    """
    Context manager for adding extra user permissions
    to the ``user_obj`` instance. This add extra permissions
    on db.

    Usage::

        # Create user for testing
        >>> from django.contrib.auth.models import User
        >>> james = User.objects.create_user(
        ...     username='permission_test_user_james2',
        ...     email='permission_test_user_james2@test.com',
        ...     password='password',
        ... )
        >>> alice = User.objects.create_user(
        ...     username='permission_test_user_alice2',
        ...     email='permission_test_user_alice2@test.com',
        ...     password='password',
        ... )

        # They does not have 'auth.add_user' and 'auth.change_usr' permission
        >>> assert not james.has_perm('auth.add_user')
        >>> assert not alice.has_perm('auth.add_user')
        >>> assert not james.has_perm('auth.change_user')
        >>> assert not alice.has_perm('auth.change_user')

        # james have the permissions
        >>> with real_permissions(james, 'auth.add_user', 'auth.change_user'):
        ...     assert james.has_perm('auth.add_user')
        ...     assert not alice.has_perm('auth.add_user')
        ...     assert james.has_perm('auth.change_user')
        ...     assert not alice.has_perm('auth.change_user')
        ...     # james DOES have permission in db
        ...     assert james.user_permissions.filter(
        ...             content_type__app_label='auth',
        ...             codename='add_user',
        ...         ).exists()

        # They does not have 'auth.add_user' and 'auth.change_usr' permission
        >>> assert not james.has_perm('auth.add_user')
        >>> assert not alice.has_perm('auth.add_user')
        >>> assert not james.has_perm('auth.change_user')
        >>> assert not alice.has_perm('auth.change_user')


    """
    def __init__(self, user_obj, *perms):
        self.user_obj = user_obj
        self.perms = perms
        # convert permission instance if necessary
        def convert_if_required(perm):
            if isinstance(perm, basestring):
                perm = perm_to_permission(perm)
            return perm
        self.perms = set([convert_if_required(p) for p in self.perms])
        self._added_permissions = []

    def __enter__(self):
        for perm in self.perms:
            if perm not in self.user_obj.user_permissions.all():
                self._added_permissions.append(perm)
                self.user_obj.user_permissions.add(perm)
        if hasattr(self.user_obj, '_perm_cache'):
            delattr(self.user_obj, '_perm_cache')
        return self.user_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.user_obj.user_permissions.remove(*self._added_permissions)
        if hasattr(self.user_obj, '_perm_cache'):
            delattr(self.user_obj, '_perm_cache')


