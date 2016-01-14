# coding=utf-8
try:
    import collections
    def isiterable(x):
        return isinstance(x, collections.Iterable)
except ImportError:
    def isiterable(x):
        try:
            iter(x)
            return True
        except TypeError:
            return False

import django
if django.VERSION >= (1, 9):
    add_to_builtins = None
else:
    try:
        from django.template.base import add_to_builtins
    except ImportError:
        from django.template.loader import add_to_builtins

try:
    # django.utils.importlib is removed from Django 1.9
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

try:
    # Django 1.7 or over use the new application loading system
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

try:
    from django.utils.module_loading import import_string
except ImportError:
    try:
        from django.utils.module_loading import import_by_path as import_string
    except ImportError:
        def import_string(dotted_path):
            try:
                module_path, class_name = dotted_path.rsplit('.', 1)
            except ValueError:
                raise ImportError(
                    "%s doesn't look like a module path" % dotted_path
                )
            module = import_module(module_path)
            try:
                return getattr(module, class_name)
            except AttributeError:
                raise ImportError(
                    'Module "%s" does not define a "%s" attribute/class' % (
                        module_path, class_name
                    ))

try:
    # Python 3
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    from urlparse import urlparse

import sys
if sys.version_info >= (3, 0):
    def isstr(x):
        return isinstance(x, str)
else:
    def isstr(x):
        return isinstance(x, basestring)

try:
    from django.util import six
except ImportError:
    # Django 1.2/1.3 does not have six
    import six
