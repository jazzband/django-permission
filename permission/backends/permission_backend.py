# vim: set fileencoding=utf-8 :
"""
Authentication backends for checking permissions

Method:
    get_permission_handler
        get permission handler of the model from registry

Class:
    PermissionBackend
        Authentication backend for checking permissions


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

from permission.handlers import registry

__all__ = ('PermissionBackend',)


class PermissionBackend(object):
    """Authentication backend for cheking permissions
    
    This backend is used to check permissions. The permissions
    are handled with ``PermissionHandler`` which have to be registered in
    ``fluidpermission.handlers.registry`` before use.

    ``has_perm(user_obj, perm, obj=None)`` method of detected model's
    ``PermissionHandler`` will be used to cheking process.

    If no model was detected or no handler was registered, this backend
    does not touch that permission and return ``None`` to pass the permission
    checking process to downstream backends.

    """
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        """This backend is only for checking permission"""
        return None

    def has_perm(self, user_obj, perm, obj=None):
        """check permission"""
        # get permission handlers fot this perm
        handlers = registry.get_handlers(perm)
        for handler in handlers:
            if handler.has_perm(user_obj, perm, obj=obj):
                return True
        # do not touch this permission
        return False

    def has_module_perms(self, user_obj, app_label):
        # get permission handlers fot this perm
        handlers = registry.get_module_handlers(app_label)
        for handler in handlers:
            if handler.has_module_perms(user_obj, app_label):
                return True
        return False
