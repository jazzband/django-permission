# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from permission.tests.utils import create_user
from permission.tests.utils import create_anonymous
from permission.tests.utils import create_group
from permission.tests.utils import create_article
from permission.tests.compatibility import MagicMock
from permission.tests.compatibility import override_settings
from permission.logics import GroupInPermissionLogic
from permission.utils.logics import add_permission_logic


@override_settings(
    PERMISSION_DEFAULT_GIPL_ANY_PERMISSION=True,
    PERMISSION_DEFAULT_GIPL_ADD_PERMISSION=True,
    PERMISSION_DEFAULT_GIPL_CHANGE_PERMISSION=True,
    PERMISSION_DEFAULT_GIPL_DELETE_PERMISSION=True,
)
class PermissionLogicsAuthorPermissionLogicTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user('john')
        self.user2 = create_user('tony')
        self.user3 = create_user('peter')
        self.anonymous = create_anonymous()
        self.group1 = create_group('admin', self.user1)
        self.group2 = create_group('staff', self.user2)
        self.perm1 = 'permission.add_article'
        self.perm2 = 'permission.change_article'
        self.perm3 = 'permission.delete_article'
        self.article = create_article('test')

    def test_constructor(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(isinstance(permission_logic, GroupInPermissionLogic))
        self.assertEqual(permission_logic.group_names, ['admin'])
        self.assertEqual(permission_logic.any_permission, True)
        self.assertEqual(permission_logic.add_permission, True)
        self.assertEqual(permission_logic.change_permission, True)
        self.assertEqual(permission_logic.delete_permission, True)

        permission_logic = GroupInPermissionLogic(['admin', 'staff'])
        self.assertTrue(isinstance(permission_logic, GroupInPermissionLogic))
        self.assertEqual(permission_logic.group_names, ['admin', 'staff'])
        self.assertEqual(permission_logic.any_permission, True)
        self.assertEqual(permission_logic.add_permission, True)
        self.assertEqual(permission_logic.change_permission, True)
        self.assertEqual(permission_logic.delete_permission, True)

    def test_constructor_with_specifing_any_permission(self):
        permission_logic = GroupInPermissionLogic('admin', any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(isinstance(permission_logic, GroupInPermissionLogic))
        self.assertEqual(permission_logic.any_permission, False)

    def test_constructor_with_specifing_add_permission(self):
        permission_logic = GroupInPermissionLogic('admin', add_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(isinstance(permission_logic, GroupInPermissionLogic))
        self.assertEqual(permission_logic.add_permission, False)

    def test_constructor_with_specifing_change_permission(self):
        permission_logic = GroupInPermissionLogic('admin', change_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(isinstance(permission_logic, GroupInPermissionLogic))
        self.assertEqual(permission_logic.change_permission, False)

    def test_constructor_with_specifing_delete_permission(self):
        permission_logic = GroupInPermissionLogic('admin', delete_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(isinstance(permission_logic, GroupInPermissionLogic))
        self.assertEqual(permission_logic.delete_permission, False)

    def test_has_perm_add_without_obj(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm1))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm1))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm1))

    def test_has_perm_change_without_obj(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm2))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm2))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm2))

    def test_has_perm_delete_without_obj(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm3))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm3))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm3))

    def test_has_perm_add_with_obj(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm1, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm1, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm1, self.article))

    def test_has_perm_change_with_obj(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm2, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm2, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm2, self.article))

    def test_has_perm_delete_with_obj(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm3, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm3, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm3, self.article))

    def test_has_perm_add_without_obj_with_anonymous(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm1))

    def test_has_perm_change_without_obj_with_anonymous(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm2))

    def test_has_perm_delete_without_obj_with_anonymous(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm3))

    def test_has_perm_add_with_obj_with_anonymous(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm1, self.article))

    def test_has_perm_change_with_obj_with_anonymous(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm2, self.article))

    def test_has_perm_delete_with_obj_with_anonymous(self):
        permission_logic = GroupInPermissionLogic('admin')
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm3, self.article))

    def test_has_perm_add_without_obj_with_two_groups(self):
        permission_logic = GroupInPermissionLogic(['admin', 'staff'])
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm1))
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm1))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm1))

    def test_has_perm_change_without_obj_with_two_groups(self):
        permission_logic = GroupInPermissionLogic(['admin', 'staff'])
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm2))
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm2))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm2))

    def test_has_perm_delete_without_obj_with_two_groups(self):
        permission_logic = GroupInPermissionLogic(['admin', 'staff'])
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm3))
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm3))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm3))

    def test_has_perm_add_with_obj_with_two_groups(self):
        permission_logic = GroupInPermissionLogic(['admin', 'staff'])
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm1, self.article))
        self.assertTrue(
                permission_logic.has_perm(self.user2, self.perm1, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm1, self.article))

    def test_has_perm_change_with_obj_with_two_groups(self):
        permission_logic = GroupInPermissionLogic(['admin', 'staff'])
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm2, self.article))
        self.assertTrue(
                permission_logic.has_perm(self.user2, self.perm2, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm2, self.article))

    def test_has_perm_delete_with_obj_with_two_groups(self):
        permission_logic = GroupInPermissionLogic(['admin', 'staff'])
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm3, self.article))
        self.assertTrue(
                permission_logic.has_perm(self.user2, self.perm3, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm3, self.article))

    def test_has_perm_add_without_obj_without_any_permission(self):
        permission_logic = GroupInPermissionLogic('admin', any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm1))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm1))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm1))

    def test_has_perm_change_without_obj_without_any_permission(self):
        permission_logic = GroupInPermissionLogic('admin', any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm2))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm2))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm2))

    def test_has_perm_delete_without_obj_without_any_permission(self):
        permission_logic = GroupInPermissionLogic('admin', any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(permission_logic.has_perm(self.user1, self.perm3))
        self.assertFalse(permission_logic.has_perm(self.user2, self.perm3))
        self.assertFalse(permission_logic.has_perm(self.user3, self.perm3))

    def test_has_perm_add_with_obj_without_any_permission(self):
        permission_logic = GroupInPermissionLogic('admin', any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm1, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm1, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm1, self.article))

    def test_has_perm_change_with_obj_without_any_permission(self):
        permission_logic = GroupInPermissionLogic('admin', any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm2, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm2, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm2, self.article))

    def test_has_perm_delete_with_obj_without_any_permission(self):
        permission_logic = GroupInPermissionLogic('admin', any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)

        self.assertTrue(
                permission_logic.has_perm(self.user1, self.perm3, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user2, self.perm3, self.article))
        self.assertFalse(
                permission_logic.has_perm(self.user3, self.perm3, self.article))

