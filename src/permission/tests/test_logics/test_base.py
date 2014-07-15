# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from permission.tests.utils import create_user
from permission.tests.utils import create_article
from permission.logics import PermissionLogic


class PermissionLogicsPermissionLogicTestCase(TestCase):

    def setUp(self):
        self.user = create_user('john')
        self.perm1 = 'permission.add_article'
        self.perm2 = 'permission.change_article'
        self.perm3 = 'permission.delete_article'
        self.article = create_article('test')

    def test_constructor(self):
        permission_logic = PermissionLogic()
        self.assertTrue(isinstance(permission_logic, PermissionLogic))

    def test_has_perm_add_wihtout_obj(self):
        permission_logic = PermissionLogic()
        self.assertRaises(NotImplementedError,
                          permission_logic.has_perm,
                          self.user, self.perm1)

    def test_has_perm_change_wihtout_obj(self):
        permission_logic = PermissionLogic()
        self.assertRaises(NotImplementedError,
                          permission_logic.has_perm,
                          self.user, self.perm2)

    def test_has_perm_delete_wihtout_obj(self):
        permission_logic = PermissionLogic()
        self.assertRaises(NotImplementedError,
                          permission_logic.has_perm,
                          self.user, self.perm3)

    def test_has_perm_add_wiht_obj(self):
        permission_logic = PermissionLogic()
        self.assertRaises(NotImplementedError,
                          permission_logic.has_perm,
                          self.user, self.perm1, self.article)

    def test_has_perm_change_wiht_obj(self):
        permission_logic = PermissionLogic()
        self.assertRaises(NotImplementedError,
                          permission_logic.has_perm,
                          self.user, self.perm2, self.article)

    def test_has_perm_delete_wiht_obj(self):
        permission_logic = PermissionLogic()
        self.assertRaises(NotImplementedError,
                          permission_logic.has_perm,
                          self.user, self.perm3, self.article)
