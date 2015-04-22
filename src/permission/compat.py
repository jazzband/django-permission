# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
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

try:
    from django.template.base import add_to_builtins
except ImportError:
    from django.template.loader import add_to_builtins

try:
    from django.utils.importlib import import_module
except ImportError:
    from importlib import import_module
