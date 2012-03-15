# vim: set fileencoding=utf-8 :
"""
Authentication backends for role system


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

from permission.models import Role

__all__ = ('RoleBackend',)


class RoleBackend(object):
    """Authentication backend for role system"""
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = True

    def authenticate(self, username, password):
        """This backend is only for checking permission"""
        return None

    def get_all_roles(self, user_obj):
        return Role.objects.filter_by_user(user_obj)

    def get_all_permissions(self, user_obj, obj=None):
        if obj is not None:
            # role permission system doesn't handle
            # object permission
            return Role.objects.none()
        if hasattr(user_obj, '_role_perm_cache'):
            return user_obj._role_perm_cache
        perms = Role.objects.get_all_permissions_of_user(user_obj)
        user_obj._role_perm_cache = perms
        return user_obj._role_perm_cache

    def has_role(self, user_obj, role):
        if user_obj.is_anonymous() or not user_obj.is_active:
            return False
        return self.get_all_roles(user_obj).filter(codename=role).exists()

    def has_perm(self, user_obj, perm, obj=None):
        if user_obj.is_anonymous() or not user_obj.is_active:
            return False
        permissions = self.get_all_permissions(user_obj, obj)
        permissions = set(["%s.%s" % (p.content_type.app_label, p.codename) for p in permissions])
        if perm in permissions:
            return True
        # do not touch this permission
        return False

    def has_module_perms(self, user_obj, app_label):
        if not user_obj.is_active:
            return False
        permissions = self.get_all_permissions(user_obj)
        permissions = set(["%s.%s" % (p.content_type.app_label, p.codename) for p in permissions])
        for perm in permissions:
            if perm[:perm.index('.')] == app_label:
                return True
        return False
