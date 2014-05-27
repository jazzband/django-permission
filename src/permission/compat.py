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
