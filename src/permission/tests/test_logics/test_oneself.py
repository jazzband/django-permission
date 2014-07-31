# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from permission.tests.utils import create_user
from permission.tests.utils import create_anonymous
from permission.tests.utils import create_article
from permission.tests.compatibility import MagicMock
from permission.tests.compatibility import override_settings
from permission import add_permission_logic
from permission.logics import OneselfPermissionLogic


@override_settings(
    PERMISSION_DEFAULT_OSPL_ANY_PERMISSION=True,
    PERMISSION_DEFAULT_OSPL_CHANGE_PERMISSION=True,
    PERMISSION_DEFAULT_OSPL_DELETE_PERMISSION=True,
)
class PermissionLogicsOneselfPermissionLogicTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user('john')
        self.user2 = create_user('tony')
        self.anonymous = create_anonymous()
        self.perm1 = 'auth.add_user'
        self.perm2 = 'auth.change_user'
        self.perm3 = 'auth.delete_user'

    def test_constructor(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, OneselfPermissionLogic))
        self.assertEqual(permission_logic.any_permission, True)
        self.assertEqual(permission_logic.change_permission, True)
        self.assertEqual(permission_logic.delete_permission, True)

    def test_constructor_with_specifying_any_permission(self):
        permission_logic = OneselfPermissionLogic(any_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, OneselfPermissionLogic))
        self.assertEqual(permission_logic.any_permission, False)

    def test_constructor_with_specifying_change_permission(self):
        permission_logic = OneselfPermissionLogic(change_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, OneselfPermissionLogic))
        self.assertEqual(permission_logic.change_permission, False)

    def test_constructor_with_specifying_delete_permission(self):
        permission_logic = OneselfPermissionLogic(delete_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, OneselfPermissionLogic))
        self.assertEqual(permission_logic.delete_permission, False)

    def test_has_perm_add_without_obj(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm1))

    def test_has_perm_change_without_obj(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm2))

    def test_has_perm_delete_without_obj(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm3))

    def test_has_perm_add_without_obj_with_anonymous(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm1))

    def test_has_perm_change_without_obj_with_anonymous(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm2))

    def test_has_perm_delete_without_obj_with_anonymous(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm3))

    def test_has_perm_add_with_obj(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
                permission_logic.has_perm(self.user1, self.perm1, self.user2))

    def test_has_perm_change_with_obj(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
                permission_logic.has_perm(self.user1, self.perm2, self.user2))

    def test_has_perm_delete_with_obj(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
                permission_logic.has_perm(self.user1, self.perm3, self.user2))

    def test_has_perm_add_with_obj_with_anonymous(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm1, self.user1))

    def test_has_perm_change_with_obj_with_anonymous(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm2, self.user1))

    def test_has_perm_delete_with_obj_with_anonymous(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm3, self.user1))

    def test_has_perm_add_with_himself(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm1, self.user1))

    def test_has_perm_change_with_himself(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm2, self.user1))

    def test_has_perm_delete_with_himself(self):
        permission_logic = OneselfPermissionLogic()
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm3, self.user1))

    def test_has_perm_add_with_himself_non_any(self):
        permission_logic = OneselfPermissionLogic(any_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
                permission_logic.has_perm(self.user1, self.perm1, self.user1))

    def test_has_perm_change_with_himself_non_any(self):
        permission_logic = OneselfPermissionLogic(any_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm2, self.user1))

    def test_has_perm_delete_with_obj_non_any(self):
        permission_logic = OneselfPermissionLogic(any_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm3, self.user1))

    def test_has_perm_add_with_himself_non_any_no_change(self):
        permission_logic = OneselfPermissionLogic(any_permission=False,
                                                 change_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
                permission_logic.has_perm(self.user1, self.perm1, self.user1))

    def test_has_perm_change_with_himself_non_any_no_change(self):
        permission_logic = OneselfPermissionLogic(any_permission=False,
                                                 change_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
                permission_logic.has_perm(self.user1, self.perm2, self.user1))

    def test_has_perm_delete_with_himself_non_any_no_change(self):
        permission_logic = OneselfPermissionLogic(any_permission=False,
                                                 change_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm3, self.user1))

    def test_has_perm_add_with_himself_non_any_no_delete(self):
        permission_logic = OneselfPermissionLogic(any_permission=False,
                                                 delete_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
                permission_logic.has_perm(self.user1, self.perm1, self.user1))

    def test_has_perm_change_with_himself_non_any_no_delete(self):
        permission_logic = OneselfPermissionLogic(any_permission=False,
                                                 delete_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm2, self.user1))

    def test_has_perm_delete_with_himself_non_any_no_delete(self):
        permission_logic = OneselfPermissionLogic(any_permission=False,
                                                 delete_permission=False)
        add_permission_logic(self.user1.__class__, permission_logic)
        self.assertFalse(
                permission_logic.has_perm(self.user1, self.perm3, self.user1))
