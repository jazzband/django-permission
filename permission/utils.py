# vim: set fileencoding=utf-8 :
"""
Utilities


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

__all__ = ('get_permission_codename', 'autodiscover',)

def get_permission_codename(perm):
    """get permission codename from permission string

    Usage:
        >>> get_permission_codename(u"app_label.codename_model")
        u"codename_model"
        >>> get_permission_codename(u"app_label.codename")
        u"codename"
        >>> get_permission_codename(u"codename_model")
        u"codename_model"
        >>> get_permission_codename(u"codename")
        u"codename"
        >>> get_permission_codename(u"app_label.app_label.codename_model")
        u"app_label.codename_model"

    """
    try:
        perm = perm.split('.', 1)[1]
    except IndexError:
        pass
    return perm

def autodiscover(module_name=None):
    """
    Auto-discover INSTALLED_APPS permissions.py modules and fail silently when
    not present. This forces an import on them to register any permissions bits
    they may want.

    """
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule
    from permission.handlers import registry

    module_name = module_name or settings.PERMISSION_MODULE_NAME

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's permissions module
        try:
            before_import_registry = copy.copy(registry._registry)
            import_module('%s.%s' % (app, module_name))
        except:
            # Reset the model registry to the state before tha last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8254)
            registry._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an permissions module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, module_name):
                raise
