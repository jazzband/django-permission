# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from permission.tests.utils import create_user
from permission.tests.utils import create_anonymous
from permission.tests.utils import create_article
from permission.tests.compatibility import override_settings
from permission.logics import StaffPermissionLogic
from permission.utils.logics import add_permission_logic


@override_settings(
    PERMISSION_DEFAULT_SPL_ANY_PERMISSION=True,
    PERMISSION_DEFAULT_SPL_ADD_PERMISSION=True,
    PERMISSION_DEFAULT_SPL_CHANGE_PERMISSION=True,
    PERMISSION_DEFAULT_SPL_DELETE_PERMISSION=True,
)
class PermissionLogicsStaffPermissionLogicTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user('john', is_staff=True)
        self.user2 = create_user('tony')
        self.anonymous = create_anonymous()
        self.perm1 = 'permission.add_article'
        self.perm2 = 'permission.change_article'
        self.perm3 = 'permission.delete_article'
        self.article = create_article('test')

    def test_constructor(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(isinstance(permission_logic, StaffPermissionLogic))
        self.assertEqual(permission_logic.any_permission, True)
        self.assertEqual(permission_logic.add_permission, True)
        self.assertEqual(permission_logic.change_permission, True)
        self.assertEqual(permission_logic.delete_permission, True)

    def test_constructor_with_specifing_any_permission(self):
        permission_logic = StaffPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, StaffPermissionLogic))
        self.assertEqual(permission_logic.any_permission, False)

    def test_constructor_with_specifing_add_permission(self):
        permission_logic = StaffPermissionLogic(add_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, StaffPermissionLogic))
        self.assertEqual(permission_logic.add_permission, False)

    def test_constructor_with_specifing_change_permission(self):
        permission_logic = StaffPermissionLogic(change_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, StaffPermissionLogic))
        self.assertEqual(permission_logic.change_permission, False)

    def test_constructor_with_specifing_delete_permission(self):
        permission_logic = StaffPermissionLogic(delete_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, StaffPermissionLogic))
        self.assertEqual(permission_logic.delete_permission, False)

    def test_has_perm_add_without_obj(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm1))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm1))

    def test_has_perm_change_without_obj(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm2))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm2))

    def test_has_perm_delete_without_obj(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm3))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm3))

    def test_has_perm_add_with_obj(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm1, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm1, self.article))

    def test_has_perm_change_with_obj(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm2, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm2, self.article))

    def test_has_perm_delete_with_obj(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm3, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm3, self.article))

    def test_has_perm_add_without_obj_with_anonymous(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm1))

    def test_has_perm_change_without_obj_with_anonymous(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm2))

    def test_has_perm_delete_without_obj_with_anonymous(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm3))

    def test_has_perm_add_with_obj_with_anonymous(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm1, self.article))

    def test_has_perm_change_with_obj_with_anonymous(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm2, self.article))

    def test_has_perm_delete_with_obj_with_anonymous(self):
        permission_logic = StaffPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm3, self.article))

    def test_has_perm_add_without_obj_without_any(self):
        permission_logic = StaffPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm1))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm1))

    def test_has_perm_change_without_obj_without_any(self):
        permission_logic = StaffPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm2))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm2))

    def test_has_perm_delete_without_obj_without_any(self):
        permission_logic = StaffPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm3))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm3))

    def test_has_perm_add_with_obj_without_any(self):
        permission_logic = StaffPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm1, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm1, self.article))

    def test_has_perm_change_with_obj_without_any(self):
        permission_logic = StaffPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm2, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm2, self.article))

    def test_has_perm_delete_with_obj_without_any(self):
        permission_logic = StaffPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm3, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm3, self.article))
