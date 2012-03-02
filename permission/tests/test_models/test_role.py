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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)

        self.assertItemsEqual(Role.objects.filter_by_user(user1), [
                role1,
            ])
        self.assertItemsEqual(Role.objects.filter_by_user(user2), [
                role1,
            ])
        self.assertItemsEqual(Role.objects.filter_by_user(user3), [
                role1, role2,
            ])
        self.assertItemsEqual(Role.objects.filter_by_user(user4), [
                role1, role3,
            ])
        self.assertItemsEqual(Role.objects.filter_by_user(user5), [
                role1, role3,
            ])
        self.assertItemsEqual(Role.objects.filter_by_user(user6), [
                role1, role3, role4,
            ])
        self.assertItemsEqual(Role.objects.filter_by_user(user7), [
                role1, role3, role5,
            ])
        self.assertItemsEqual(Role.objects.filter_by_user(user8), [
                role1, role6,
            ])

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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
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

        self.assertItemsEqual(Role.objects.get_all_permissions_of_user(user1), [
                perm1, perm2,
            ])
        self.assertItemsEqual(Role.objects.get_all_permissions_of_user(user2), [
                perm1, perm2,
            ])
        self.assertItemsEqual(Role.objects.get_all_permissions_of_user(user3), [
                perm1, perm2, perm3,
            ])
        self.assertItemsEqual(Role.objects.get_all_permissions_of_user(user4), [
                perm1, perm2, perm4, perm5,
            ])
        self.assertItemsEqual(Role.objects.get_all_permissions_of_user(user5), [
                perm1, perm2, perm4, perm5,
            ])
        self.assertItemsEqual(Role.objects.get_all_permissions_of_user(user6), [
                perm1, perm2, perm4, perm5, perm6,
            ])
        self.assertItemsEqual(Role.objects.get_all_permissions_of_user(user7), [
                perm1, perm2, perm4, perm5, perm7,
            ])
        self.assertItemsEqual(Role.objects.get_all_permissions_of_user(user8), [
                perm1, perm2, perm8,
            ])



class PermissionRoleModelTestCase(TestCase):

    def testcreate(self):
        role = create_role('permission_test_role1')
        self.assertItemsEqual(role.name, 'permission_test_role1')
        self.assertItemsEqual(role.codename, 'permission_test_role1')
        self.assertItemsEqual(role.description, 'permission_test_role1')

        return role

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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)

        self.assertItemsEqual(role1.users, [
                user1, user2, user3, user4,
                user5, user6, user7, user8,
            ])
        self.assertItemsEqual(role2.users, [
                user3,
            ])
        self.assertItemsEqual(role3.users, [
                user4, user5, user6, user7,
            ])
        self.assertItemsEqual(role4.users, [
                user6,
            ])
        self.assertItemsEqual(role5.users, [
                user7,
            ])
        self.assertItemsEqual(role6.users, [
                user8,
            ])

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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1._permissions.add(perm1, perm2)
        role2._permissions.add(perm3)
        role3._permissions.add(perm4, perm5)
        role4._permissions.add(perm6)
        role5._permissions.add(perm7)
        role6._permissions.add(perm8)

        self.assertItemsEqual(role1.permissions, [
                perm1, perm2
            ])
        self.assertItemsEqual(role2.permissions, [
                perm1, perm2, perm3,
            ])
        self.assertItemsEqual(role3.permissions, [
                perm1, perm2, perm4, perm5,
            ])
        self.assertItemsEqual(role4.permissions, [
                perm1, perm2, perm4, perm5, perm6,
            ])
        self.assertItemsEqual(role5.permissions, [
                perm1, perm2, perm4, perm5, perm7,
            ])
        self.assertItemsEqual(role6.permissions, [
                perm1, perm2, perm8,
            ])

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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1.users.add(user1, user2)
        role2.users.add(user3)
        role3.users.add(user4, user5)
        role4.users.add(user6)
        role5.users.add(user7)
        role6.users.add(user8)

        self.assertItemsEqual(role1._users.all(), [
                user1, user2,
            ])
        self.assertItemsEqual(role2._users.all(), [
                user3,
            ])
        self.assertItemsEqual(role3._users.all(), [
                user4, user5,
            ])
        self.assertItemsEqual(role4._users.all(), [
                user6,
            ])
        self.assertItemsEqual(role5._users.all(), [
                user7,
            ])
        self.assertItemsEqual(role6._users.all(), [
                user8,
            ])

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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)
        role1.users.remove(user1, user2)
        role2.users.remove(user3)
        role3.users.remove(user4, user5)
        role4.users.remove(user6)
        role5.users.remove(user7)
        role6.users.remove(user8)

        self.assertItemsEqual(role1._users.all(), [])
        self.assertItemsEqual(role2._users.all(), [])
        self.assertItemsEqual(role3._users.all(), [])
        self.assertItemsEqual(role4._users.all(), [])
        self.assertItemsEqual(role5._users.all(), [])
        self.assertItemsEqual(role6._users.all(), [])

    def test_clear_users(self):
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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1._users.add(user1, user2)
        role2._users.add(user3)
        role3._users.add(user4, user5)
        role4._users.add(user6)
        role5._users.add(user7)
        role6._users.add(user8)
        role1.users.clear()
        role2.users.clear()
        role3.users.clear()
        role4.users.clear()
        role5.users.clear()
        role6.users.clear()

        self.assertItemsEqual(role1._users.all(), [])
        self.assertItemsEqual(role2._users.all(), [])
        self.assertItemsEqual(role3._users.all(), [])
        self.assertItemsEqual(role4._users.all(), [])
        self.assertItemsEqual(role5._users.all(), [])
        self.assertItemsEqual(role6._users.all(), [])


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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1.permissions.add(perm1, perm2)
        role2.permissions.add(perm3)
        role3.permissions.add(perm4, perm5)
        role4.permissions.add(perm6)
        role5.permissions.add(perm7)
        role6.permissions.add(perm8)

        self.assertItemsEqual(role1._permissions.all(), [
                perm1, perm2,
            ])
        self.assertItemsEqual(role2._permissions.all(), [
                perm3,
            ])
        self.assertItemsEqual(role3._permissions.all(), [
                perm4, perm5,
            ])
        self.assertItemsEqual(role4._permissions.all(), [
                perm6,
            ])
        self.assertItemsEqual(role5._permissions.all(), [
                perm7,
            ])
        self.assertItemsEqual(role6._permissions.all(), [
                perm8,
            ])


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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1._permissions.add(perm1, perm2)
        role2._permissions.add(perm3)
        role3._permissions.add(perm4, perm5)
        role4._permissions.add(perm6)
        role5._permissions.add(perm7)
        role6._permissions.add(perm8)
        role1.permissions.remove(perm1, perm2)
        role2.permissions.remove(perm3)
        role3.permissions.remove(perm4, perm5)
        role4.permissions.remove(perm6)
        role5.permissions.remove(perm7)
        role6.permissions.remove(perm8)

        self.assertItemsEqual(role1._permissions.all(), [])
        self.assertItemsEqual(role2._permissions.all(), [])
        self.assertItemsEqual(role3._permissions.all(), [])
        self.assertItemsEqual(role4._permissions.all(), [])
        self.assertItemsEqual(role5._permissions.all(), [])
        self.assertItemsEqual(role6._permissions.all(), [])

    def test_clear_permissions(self):
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
        role2 = create_role('permission_test_role2', role1)
        role3 = create_role('permission_test_role3', role1)
        role4 = create_role('permission_test_role4', role3)
        role5 = create_role('permission_test_role5', role3)
        role6 = create_role('permission_test_role6', role1)
        role1._permissions.add(perm1, perm2)
        role2._permissions.add(perm3)
        role3._permissions.add(perm4, perm5)
        role4._permissions.add(perm6)
        role5._permissions.add(perm7)
        role6._permissions.add(perm8)
        role1.permissions.clear()
        role2.permissions.clear()
        role3.permissions.clear()
        role4.permissions.clear()
        role5.permissions.clear()
        role6.permissions.clear()

        self.assertItemsEqual(role1._permissions.all(), [])
        self.assertItemsEqual(role2._permissions.all(), [])
        self.assertItemsEqual(role3._permissions.all(), [])
        self.assertItemsEqual(role4._permissions.all(), [])
        self.assertItemsEqual(role5._permissions.all(), [])
        self.assertItemsEqual(role6._permissions.all(), [])
