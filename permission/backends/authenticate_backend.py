# vim: set fileencoding=utf-8 :
"""
short module explanation


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
from django.contrib.auth.backends import ModelBackend as AuthModelBackend
from django.contrib.auth.backends import RemoteUserBackend as AuthRemoteUserBackend

class ModelBackend(AuthModelBackend):
    def get_group_permissions(self, user_obj, obj=None):
        """With django-permission, group permission is not available."""
        return set()
    def get_all_permissions(self, user_obj, obj=None):
        """with django-permission, user permission is not available."""
        return set()
    def has_perm(self, user_obj, perm, obj=None):
        """with django-permission, permission check is handled by PermissionBackend"""
        return False
    def has_module_perms(self, user_obj, app_label):
        """with django-permission, permission check is handled by PermissionBackend"""
        return False

class RemoteUserBackend(AuthRemoteUserBackend):
    def get_group_permissions(self, user_obj, obj=None):
        """With django-permission, group permission is not available."""
        return set()
    def get_all_permissions(self, user_obj, obj=None):
        """with django-permission, user permission is not available."""
        return set()
    def has_perm(self, user_obj, perm, obj=None):
        """with django-permission, permission check is handled by PermissionBackend"""
        return False
    def has_module_perms(self, user_obj, app_label):
        """with django-permission, permission check is handled by PermissionBackend"""
        return False

