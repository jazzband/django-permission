# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import doctest
import unittest

list_of_doctests = [
    'permission.backends',
    'permission.handlers',
    'permission.logics.base',
    'permission.logics.author',
    'permission.logics.collaborators',
    'permission.utils.handlers',
    'permission.utils.logics',
    'permission.utils.permissions',
]
list_of_unittests = [
    'permission.tests.test_utils.test_logics',
    'permission.tests.test_utils.test_handlers',
    'permission.tests.test_logics.test_base',
    'permission.tests.test_logics.test_author',
    'permission.tests.test_logics.test_collaborators',
    'permission.tests.test_templatetags.test_permissionif',
    'permission.tests.test_backends',
    'permission.tests.test_handlers',
]

def suite():
    suite = unittest.TestSuite()
    for t in list_of_doctests:
        suite.addTest(doctest.DocTestSuite(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    for t in list_of_unittests:
        suite.addTest(unittest.TestLoader().loadTestsFromModule(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    return suite
