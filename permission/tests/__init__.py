from __future__ import with_statement
import doctest
import unittest
from permission.tests.utils import *
from permission.patches.cmp_patch import *

list_of_doctests = [
    'permission.utils',
    'permission.utils.converters',
    'permission.utils.test.context_managers',
]
list_of_unittests = [
    'permission.tests.test_models',
    'permission.tests.test_handlers',
    'permission.tests.test_backends',
    'permission.tests.test_decorators',
    'permission.tests.test_templatetags',
]

def suite():
    _suite = unittest.TestSuite()
    for t in list_of_doctests:
        _suite.addTest(doctest.DocTestSuite(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    for t in list_of_unittests:
        _suite.addTest(unittest.TestLoader().loadTestsFromModule(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    return _suite
