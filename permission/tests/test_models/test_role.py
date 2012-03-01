# vim: set fileencoding=utf-8 :
"""
Unittest module of ...


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
from django.test import TestCase

from permission.models import Role
from permission.tests.utils import create_user
from permission.tests.utils import create_role
from permission.tests.utils import create_permission


class PermissionRoleManagerTestCase(TestCase):

    def test_filter_by_user(self):
        # role1           -- user1, user2
        #   +- role2      -- user3
        #   +- role3      -- user4, user5
        #   |    +- role4 -- user6
        #   |    +- role5 -- user7
        #   +- role6      -- user8
        user1 = create_user('permission_test_user1')
        user2 = create_user('permission_test_user2')
        user3 = create_user('permission_test_user3')
        user4 = create_user('permission_test_user4')
        user5 = create_user('permission_test_user5')
        user6 = create_user('permission_test_user6')
        user7 = create_user('permission_test_user7')
        user8 = create_user('permission_test_user8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)

        self.assertEqual(frozenset(Role.objects.filter_by_user(user1)), frozenset([
                role1, role2, role3, role4, role5, role6
            ]))
        self.assertEqual(frozenset(Role.objects.filter_by_user(user2)), frozenset([
                role1, role2, role3, role4, role5, role6
            ]))
        self.assertEqual(frozenset(Role.objects.filter_by_user(user3)), frozenset([
                role2,
            ]))
        self.assertEqual(frozenset(Role.objects.filter_by_user(user4)), frozenset([
                role3, role4, role5,
            ]))
        self.assertEqual(frozenset(Role.objects.filter_by_user(user5)), frozenset([
                role3, role4, role5,
            ]))
        self.assertEqual(frozenset(Role.objects.filter_by_user(user6)), frozenset([
                role4,
            ]))
        self.assertEqual(frozenset(Role.objects.filter_by_user(user7)), frozenset([
                role5,
            ]))
        self.assertEqual(frozenset(Role.objects.filter_by_user(user8)), frozenset([
                role6,
            ]))

    def test_get_all_permissions_of_user(self):
        # role1           -- user1, user2 -- perm1, perm2
        #   +- role2      -- user3        -- perm3
        #   +- role3      -- user4, user5 -- perm4, perm5
        #   |    +- role4 -- user6        -- perm6
        #   |    +- role5 -- user7        -- perm7
        #   +- role6      -- user8        -- perm8
        user1 = create_user('permission_test_user1')
        user2 = create_user('permission_test_user2')
        user3 = create_user('permission_test_user3')
        user4 = create_user('permission_test_user4')
        user5 = create_user('permission_test_user5')
        user6 = create_user('permission_test_user6')
        user7 = create_user('permission_test_user7')
        user8 = create_user('permission_test_user8')
        perm1 = create_permission('permission_test_perm1')
        perm2 = create_permission('permission_test_perm2')
        perm3 = create_permission('permission_test_perm3')
        perm4 = create_permission('permission_test_perm4')
        perm5 = create_permission('permission_test_perm5')
        perm6 = create_permission('permission_test_perm6')
        perm7 = create_permission('permission_test_perm7')
        perm8 = create_permission('permission_test_perm8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)
        role1._permissions.add(perm1, perm2)
        role2._permissions.add(perm3)
        role3._permissions.add(perm4, perm5)
        role4._permissions.add(perm6)
        role5._permissions.add(perm7)
        role6._permissions.add(perm8)

        self.assertEqual(frozenset(Role.objects.get_all_permissions_of_user(user1)), frozenset([
                perm1, perm2, perm3, perm4,
                perm5, perm6, perm7, perm8,
            ]))
        self.assertEqual(frozenset(Role.objects.get_all_permissions_of_user(user2)), frozenset([
                perm1, perm2, perm3, perm4,
                perm5, perm6, perm7, perm8,
            ]))
        self.assertEqual(frozenset(Role.objects.get_all_permissions_of_user(user3)), frozenset([
                perm3,
            ]))
        self.assertEqual(frozenset(Role.objects.get_all_permissions_of_user(user4)), frozenset([
                perm4, perm5, perm6, perm7,
            ]))
        self.assertEqual(frozenset(Role.objects.get_all_permissions_of_user(user5)), frozenset([
                perm4, perm5, perm6, perm7,
            ]))
        self.assertEqual(frozenset(Role.objects.get_all_permissions_of_user(user6)), frozenset([
                perm6,
            ]))
        self.assertEqual(frozenset(Role.objects.get_all_permissions_of_user(user7)), frozenset([
                perm7,
            ]))
        self.assertEqual(frozenset(Role.objects.get_all_permissions_of_user(user8)), frozenset([
                perm8,
            ]))



class PermissionRoleModelTestCase(TestCase):

    def testcreate(self):
        role = create_role('permission_test_role1')
        self.assertEqual(role.name, 'permission_test_role1')
        self.assertEqual(role.codename, 'permission_test_role1')
        self.assertEqual(role.description, 'permission_test_role1')

        return role

    def test__get_all_subroles(self):
        # role1
        #   +- role2
        #   |    +- role3
        #   |    +- role4
        #   |    |   +- role5
        #   |    |   +- role6
        #   |    +- role7
        #   |         +- role8
        #   +- role9
        #        +- role10
        #        +- role11
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role7 = create_role('permission_test_role7')
        role8 = create_role('permission_test_role8')
        role9 = create_role('permission_test_role9')
        role10 = create_role('permission_test_role10')
        role11 = create_role('permission_test_role11')
        role1._subroles.add(role2, role9)
        role2._subroles.add(role3, role4, role7)
        role4._subroles.add(role5, role6)
        role7._subroles.add(role8)
        role9._subroles.add(role10, role11)

        self.assertEqual(role1.subroles, frozenset([
                role2, role3, role4, role5,
                role6, role7, role8, role9, role10, role11,
            ]))
        self.assertEqual(role2.subroles, frozenset([
                role3, role4, role5,
                role6, role7, role8,
            ]))
        self.assertEqual(role3.subroles, frozenset([]))
        self.assertEqual(role4.subroles, frozenset([
                role5, role6,
            ]))
        self.assertEqual(role5.subroles, frozenset([]))
        self.assertEqual(role6.subroles, frozenset([]))
        self.assertEqual(role7.subroles, frozenset([
                role8,
            ]))
        self.assertEqual(role8.subroles, frozenset([]))
        self.assertEqual(role9.subroles, frozenset([
                role10, role11,
            ]))
        self.assertEqual(role10.subroles, frozenset([]))
        self.assertEqual(role11.subroles, frozenset([]))

    def test__get_all_roles(self):
        # role1
        #   +- role2
        #   |    +- role3
        #   |    +- role4
        #   |    |   +- role5
        #   |    |   +- role6
        #   |    +- role7
        #   |         +- role8
        #   +- role9
        #        +- role10
        #        +- role11
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role7 = create_role('permission_test_role7')
        role8 = create_role('permission_test_role8')
        role9 = create_role('permission_test_role9')
        role10 = create_role('permission_test_role10')
        role11 = create_role('permission_test_role11')
        role1._subroles.add(role2, role9)
        role2._subroles.add(role3, role4, role7)
        role4._subroles.add(role5, role6)
        role7._subroles.add(role8)
        role9._subroles.add(role10, role11)

        self.assertEqual(role1.roles, frozenset([
                role1, role2, role3, role4, role5,
                role6, role7, role8, role9, role10, role11,
            ]))
        self.assertEqual(role2.roles, frozenset([
                role2, role3, role4, role5,
                role6, role7, role8,
            ]))
        self.assertEqual(role3.roles, frozenset([role3]))
        self.assertEqual(role4.roles, frozenset([
                role4, role5, role6,
            ]))
        self.assertEqual(role5.roles, frozenset([role5]))
        self.assertEqual(role6.roles, frozenset([role6]))
        self.assertEqual(role7.roles, frozenset([
                role7, role8,
            ]))
        self.assertEqual(role8.roles, frozenset([role8]))
        self.assertEqual(role9.roles, frozenset([
                role9, role10, role11,
            ]))
        self.assertEqual(role10.roles, frozenset([role10]))
        self.assertEqual(role11.roles, frozenset([role11]))

    def test__get_all_users(self):
        # role1           -- user1, user2
        #   +- role2      -- user3
        #   +- role3      -- user4, user5
        #   |    +- role4 -- user6
        #   |    +- role5 -- user7
        #   +- role6      -- user8
        user1 = create_user('permission_test_user1')
        user2 = create_user('permission_test_user2')
        user3 = create_user('permission_test_user3')
        user4 = create_user('permission_test_user4')
        user5 = create_user('permission_test_user5')
        user6 = create_user('permission_test_user6')
        user7 = create_user('permission_test_user7')
        user8 = create_user('permission_test_user8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)

        self.assertEqual(frozenset(role1.users), frozenset([
                user1, user2, user3, user4,
                user5, user6, user7, user8,
            ]))
        self.assertEqual(frozenset(role2.users), frozenset([
                user3,
            ]))
        self.assertEqual(frozenset(role3.users), frozenset([
                user4, user5, user6, user7,
            ]))
        self.assertEqual(frozenset(role4.users), frozenset([
                user6,
            ]))
        self.assertEqual(frozenset(role5.users), frozenset([
                user7,
            ]))
        self.assertEqual(frozenset(role6.users), frozenset([
                user8,
            ]))

    def test__get_all_permissions(self):
        # role1           -- perm1, perm2
        #   +- role2      -- perm3
        #   +- role3      -- perm4, perm5
        #   |    +- role4 -- perm6
        #   |    +- role5 -- perm7
        #   +- role6      -- perm8
        perm1 = create_permission('permission_test_perm1')
        perm2 = create_permission('permission_test_perm2')
        perm3 = create_permission('permission_test_perm3')
        perm4 = create_permission('permission_test_perm4')
        perm5 = create_permission('permission_test_perm5')
        perm6 = create_permission('permission_test_perm6')
        perm7 = create_permission('permission_test_perm7')
        perm8 = create_permission('permission_test_perm8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._permissions.add(perm1, perm2)
        role2._permissions.add(perm3)
        role3._permissions.add(perm4, perm5)
        role4._permissions.add(perm6)
        role5._permissions.add(perm7)
        role6._permissions.add(perm8)

        self.assertEqual(frozenset(role1.permissions), frozenset([
                perm1, perm2, perm3, perm4,
                perm5, perm6, perm7, perm8,
            ]))
        self.assertEqual(frozenset(role2.permissions), frozenset([
                perm3,
            ]))
        self.assertEqual(frozenset(role3.permissions), frozenset([
                perm4, perm5, perm6, perm7,
            ]))
        self.assertEqual(frozenset(role4.permissions), frozenset([
                perm6,
            ]))
        self.assertEqual(frozenset(role5.permissions), frozenset([
                perm7,
            ]))
        self.assertEqual(frozenset(role6.permissions), frozenset([
                perm8,
            ]))

    def test_is_belong(self):
        # role1           -- user1, user2
        #   +- role2      -- user3
        #   +- role3      -- user4, user5
        #   |    +- role4 -- user6
        #   |    +- role5 -- user7
        #   +- role6      -- user8
        user1 = create_user('permission_test_user1')
        user2 = create_user('permission_test_user2')
        user3 = create_user('permission_test_user3')
        user4 = create_user('permission_test_user4')
        user5 = create_user('permission_test_user5')
        user6 = create_user('permission_test_user6')
        user7 = create_user('permission_test_user7')
        user8 = create_user('permission_test_user8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)

        self.assertTrue(role1.is_belong(user1))
        self.assertTrue(role1.is_belong(user2))
        self.assertTrue(role1.is_belong(user3))
        self.assertTrue(role1.is_belong(user4))
        self.assertTrue(role1.is_belong(user5))
        self.assertTrue(role1.is_belong(user6))
        self.assertTrue(role1.is_belong(user7))
        self.assertTrue(role1.is_belong(user8))

        self.assertFalse(role2.is_belong(user1))
        self.assertFalse(role2.is_belong(user2))
        self.assertTrue(role2.is_belong(user3))
        self.assertFalse(role2.is_belong(user4))
        self.assertFalse(role2.is_belong(user5))
        self.assertFalse(role2.is_belong(user6))
        self.assertFalse(role2.is_belong(user7))
        self.assertFalse(role2.is_belong(user8))

        self.assertFalse(role3.is_belong(user1))
        self.assertFalse(role3.is_belong(user2))
        self.assertFalse(role3.is_belong(user3))
        self.assertTrue(role3.is_belong(user4))
        self.assertTrue(role3.is_belong(user5))
        self.assertTrue(role3.is_belong(user6))
        self.assertTrue(role3.is_belong(user7))
        self.assertFalse(role3.is_belong(user8))

    def test_add_users(self):
        # role1           -- user1, user2
        #   +- role2      -- user3
        #   +- role3      -- user4, user5
        #   |    +- role4 -- user6
        #   |    +- role5 -- user7
        #   +- role6      -- user8
        user1 = create_user('permission_test_user1')
        user2 = create_user('permission_test_user2')
        user3 = create_user('permission_test_user3')
        user4 = create_user('permission_test_user4')
        user5 = create_user('permission_test_user5')
        user6 = create_user('permission_test_user6')
        user7 = create_user('permission_test_user7')
        user8 = create_user('permission_test_user8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)

        # actually role1 doesn't have user3
        self.assertFalse(role1._users.filter(pk=user3.pk).exists())
        # but user3 is in the subroles of role1 thus add_users doesn't add
        role1.add_users(user3)
        self.assertFalse(role1._users.filter(pk=user3.pk).exists())

        # role2 doesn't have user2
        self.assertFalse(role2._users.filter(pk=user2.pk).exists())
        # and no subroles have user2 thus add_users add user2 to role2
        role2.add_users(user2)
        self.assertTrue(role2._users.filter(pk=user2.pk).exists())

    def test_remove_users(self):
        # role1           -- user1, user2
        #   +- role2      -- user3
        #   +- role3      -- user4, user5
        #   |    +- role4 -- user6
        #   |    +- role5 -- user7
        #   +- role6      -- user8
        user1 = create_user('permission_test_user1')
        user2 = create_user('permission_test_user2')
        user3 = create_user('permission_test_user3')
        user4 = create_user('permission_test_user4')
        user5 = create_user('permission_test_user5')
        user6 = create_user('permission_test_user6')
        user7 = create_user('permission_test_user7')
        user8 = create_user('permission_test_user8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)

        # actually role1 doesn't have user3
        self.assertFalse(role1._users.filter(pk=user3.pk).exists())
        # thus remove_user doesn't remove even user3 is in subroles
        role1.remove_users(user3)
        self.assertFalse(role1._users.filter(pk=user3.pk).exists())
        self.assertTrue(role1.users.filter(pk=user3.pk).exists())

        # role2 have user3
        self.assertTrue(role2._users.filter(pk=user3.pk).exists())
        # thus remove_user remove user3
        role2.remove_users(user3)
        self.assertFalse(role2._users.filter(pk=user3.pk).exists())
        self.assertFalse(role2.users.filter(pk=user3.pk).exists())
        self.assertFalse(role1.users.filter(pk=user3.pk).exists())

    def test_add_permissions(self):
        # role1           -- perm1, perm2
        #   +- role2      -- perm3
        #   +- role3      -- perm4, perm5
        #   |    +- role4 -- perm6
        #   |    +- role5 -- perm7
        #   +- role6      -- perm8
        perm1 = create_permission('permission_test_perm1')
        perm2 = create_permission('permission_test_perm2')
        perm3 = create_permission('permission_test_perm3')
        perm4 = create_permission('permission_test_perm4')
        perm5 = create_permission('permission_test_perm5')
        perm6 = create_permission('permission_test_perm6')
        perm7 = create_permission('permission_test_perm7')
        perm8 = create_permission('permission_test_perm8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._permissions.add(perm1, perm2)
        role2._permissions.add(perm3)
        role3._permissions.add(perm4, perm5)
        role4._permissions.add(perm6)
        role5._permissions.add(perm7)
        role6._permissions.add(perm8)

        # actually role1 doesn't have perm3
        self.assertFalse(role1._permissions.filter(pk=perm3.pk).exists())
        # but perm3 is in the subroles of role1 thus add_permissions doesn't add
        role1.add_permissions(perm3)
        self.assertFalse(role1._permissions.filter(pk=perm3.pk).exists())

        # role2 doesn't have perm2
        self.assertFalse(role2._permissions.filter(pk=perm2.pk).exists())
        # and no subroles have perm2 thus add_perms add perm2 to role2
        role2.add_permissions(perm2)
        self.assertTrue(role2._permissions.filter(pk=perm2.pk).exists())

    def test_remove_permissions(self):
        # role1           -- perm1, perm2
        #   +- role2      -- perm3
        #   +- role3      -- perm4, perm5
        #   |    +- role4 -- perm6
        #   |    +- role5 -- perm7
        #   +- role6      -- perm8
        perm1 = create_permission('permission_test_perm1')
        perm2 = create_permission('permission_test_perm2')
        perm3 = create_permission('permission_test_perm3')
        perm4 = create_permission('permission_test_perm4')
        perm5 = create_permission('permission_test_perm5')
        perm6 = create_permission('permission_test_perm6')
        perm7 = create_permission('permission_test_perm7')
        perm8 = create_permission('permission_test_perm8')
        role1 = create_role('permission_test_role1')
        role2 = create_role('permission_test_role2')
        role3 = create_role('permission_test_role3')
        role4 = create_role('permission_test_role4')
        role5 = create_role('permission_test_role5')
        role6 = create_role('permission_test_role6')
        role1._subroles.add(role2, role3, role6)
        role3._subroles.add(role4, role5)
        role1._permissions.add(perm1, perm2)
        role2._permissions.add(perm3)
        role3._permissions.add(perm4, perm5)
        role4._permissions.add(perm6)
        role5._permissions.add(perm7)
        role6._permissions.add(perm8)

        # actually role1 doesn't have perm3
        self.assertFalse(role1._permissions.filter(pk=perm3.pk).exists())
        # thus remove_perm doesn't remove even perm3 is in subroles
        role1.remove_permissions(perm3)
        self.assertFalse(role1._permissions.filter(pk=perm3.pk).exists())
        self.assertTrue(role1.permissions.filter(pk=perm3.pk).exists())

        # role2 have perm3
        self.assertTrue(role2._permissions.filter(pk=perm3.pk).exists())
        # thus remove_perm remove perm3
        role2.remove_permissions(perm3)
        self.assertFalse(role2._permissions.filter(pk=perm3.pk).exists())
        self.assertFalse(role2.permissions.filter(pk=perm3.pk).exists())
        self.assertFalse(role1.permissions.filter(pk=perm3.pk).exists())

