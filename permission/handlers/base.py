# vim: set fileencoding=utf-8 :
"""
Permission handler base


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

__all__ = ('PermissionHandler',)


class PermissionHandler(object):
    """Permission handler base class.

    You must create subclasses of this to create your custom permission handler.
    And you MUST DEFINE ``has_perm(user_obj, perm, obj=None)`` method to check
    the permission of passed ``user_obj``

    ``get_permissions()`` method is used to determine which permission strings are
    should be handled with this handler. In default, this method return the value
    of ``permissions`` attribute if defined. Otherwise it return the same value as
    ``get_model_permissions()`` method which described below.

    ``get_model_permissions()`` method return permission strings which is related
    to the ``model`` registered with this handler instance. ``get_app_permissions()``
    method return permission strings which is related to the app of the ``model``
    registered with this handler instance.

    ``get_permission_codename(perm)`` method return codename of ``perm``.

    """
    def __init__(self, model):
        self.model = model

    def get_app_permissions(self):
        """get permissions associated with app of this model"""
        if not hasattr(self, '_app_perm_cache'):
            app_label = self.model._meta.app_label
            qs = Permission.objects.filter(content_type__app_label=app_label)
            app_perms = set([u"%s.%s" % (app_label, p.codename) for p in qs.iterator()])
            self._app_perm_cache = app_perms
        return set(self._app_perm_cache)

    def get_model_permissions(self):
        """get permissions associated with this model"""
        if not hasattr(self, '_model_perm_cache'):
            app_label = self.model._meta.app_label
            model = self.model._meta.object_name.lower()
            qs = Permission.objects.filter(
                        content_type__app_label=app_label,
                        content_type__model=model
                    )
            model_perms = set([u"%s.%s" % (app_label, p.codename) for p in qs.iterator()])
            self._model_perm_cache = model_perms
        return set(self._model_perm_cache)

    def get_permissions(self):
        """get permissions which this handler will handle"""
        if not hasattr(self, 'permissions'):
            # build permission list associated with the model
            self.permissions = self.get_model_permissions()
        return set(self.permissions)

    def get_permission_codename(self, perm):
        """get permission codename from permission string"""
        from permission.utils import get_permission_codename
        return get_permission_codename(perm)

    def has_perm(self, user_obj, perm, obj=None):
        """whether the ``user_obj`` has permission ``perm`` of ``obj``

        This method will be called in ``has_perm()`` method of authentication
        backend so you CAN NOT call ``user_obj.has_perm()`` method within
        this method.

        Subclasses must override this method to define them own checking process.

        """
        raise NotImplementedError(
                '"%s" does not have ``has_perm`` method. Subclasses must '
                'define ``has_perm(user_obj, perm, obj=None)`` method.'
            )

    def has_module_perm(self, user_obj, app_label):
        return False
