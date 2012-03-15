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

from permission.backends import RoleBackend
from permission.utils import permission_to_perm
from permission.tests import create_user
from permission.tests import create_role
from permission.tests import create_permission

class PermissionRoleBackendTestCase(TestCase):

    def setUp(self):
        # role1           -- user1, user2 -- perm1, perm2
        #   +- role2      -- user3        -- perm3
        #   +- role3      -- user4, user5 -- perm4, perm5
        #   |    +- role4 -- user6        -- perm6
        #   |    +- role5 -- user7        -- perm7
        #   +- role6      -- user8        -- perm8
        self.user1 = user1 = create_user('permission_test_user1')
        self.user2 = user2 = create_user('permission_test_user2')
        self.user3 = user3 = create_user('permission_test_user3')
        self.user4 = user4 = create_user('permission_test_user4')
        self.user5 = user5 = create_user('permission_test_user5')
        self.user6 = user6 = create_user('permission_test_user6')
        self.user7 = user7 = create_user('permission_test_user7')
        self.user8 = user8 = create_user('permission_test_user8')
        self.perm1 = perm1 = create_permission('permission_test_perm1')
        self.perm2 = perm2 = create_permission('permission_test_perm2')
        self.perm3 = perm3 = create_permission('permission_test_perm3')
        self.perm4 = perm4 = create_permission('permission_test_perm4')
        self.perm5 = perm5 = create_permission('permission_test_perm5')
        self.perm6 = perm6 = create_permission('permission_test_perm6')
        self.perm7 = perm7 = create_permission('permission_test_perm7')
        self.perm8 = perm8 = create_permission('permission_test_perm8')
        self.role1 = role1 = create_role('permission_test_role1')
        self.role2 = role2 = create_role('permission_test_role2', role1)
        self.role3 = role3 = create_role('permission_test_role3', role1)
        self.role4 = role4 = create_role('permission_test_role4', role3)
        self.role5 = role5 = create_role('permission_test_role5', role3)
        self.role6 = role6 = create_role('permission_test_role6', role1)
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

    def test_attributes_required(self):
        backend = RoleBackend()

        self.assertTrue(hasattr(backend, 'supports_object_permissions'))
        self.assertFalse(getattr(backend, 'supports_object_permissions'))

        self.assertTrue(hasattr(backend, 'supports_anonymous_user'))
        self.assertFalse(getattr(backend, 'supports_anonymous_user'))

        self.assertTrue(hasattr(backend, 'supports_inactive_user'))
        self.assertTrue(getattr(backend, 'supports_inactive_user'))

        self.assertTrue(hasattr(backend, 'authenticate'))
        self.assertEqual(backend.authenticate(None, None), None)

        self.assertTrue(hasattr(backend, 'has_perm'))
        self.assertTrue(hasattr(backend, 'has_role'))
        self.assertTrue(hasattr(backend, 'get_all_roles'))

    def test_get_all_roles(self):
        backend = RoleBackend()
        
        user1, user2, user3, user4 = self.user1, self.user2, self.user3, self.user4
        user5, user6, user7, user8 = self.user5, self.user6, self.user7, self.user8
        role1, role2, role3 = self.role1, self.role2, self.role3
        role4, role5, role6 = self.role4, self.role5, self.role6

        self.assertItemsEqual(backend.get_all_roles(user1), [
                role1,
            ])
        self.assertItemsEqual(backend.get_all_roles(user2), [
                role1,
            ])
        self.assertItemsEqual(backend.get_all_roles(user3), [
                role1, role2,
            ])
        self.assertItemsEqual(backend.get_all_roles(user4), [
                role1, role3,
            ])
        self.assertItemsEqual(backend.get_all_roles(user5), [
                role1, role3,
            ])
        self.assertItemsEqual(backend.get_all_roles(user6), [
                role1, role3, role4,
            ])
        self.assertItemsEqual(backend.get_all_roles(user7), [
                role1, role3, role5,
            ])
        self.assertItemsEqual(backend.get_all_roles(user8), [
                role1, role6,
            ])

    def test_get_all_permissions(self):
        backend = RoleBackend()
        
        user1, user2, user3, user4 = self.user1, self.user2, self.user3, self.user4
        user5, user6, user7, user8 = self.user5, self.user6, self.user7, self.user8
        perm1, perm2, perm3, perm4 = self.perm1, self.perm2, self.perm3, self.perm4
        perm5, perm6, perm7, perm8 = self.perm5, self.perm6, self.perm7, self.perm8

        perm1 = permission_to_perm(perm1)
        perm2 = permission_to_perm(perm2)
        perm3 = permission_to_perm(perm3)
        perm4 = permission_to_perm(perm4)
        perm5 = permission_to_perm(perm5)
        perm6 = permission_to_perm(perm6)
        perm7 = permission_to_perm(perm7)
        perm8 = permission_to_perm(perm8)

        self.assertItemsEqual(backend.get_all_permissions(user1), [
                perm1, perm2,
            ])
        self.assertItemsEqual(backend.get_all_permissions(user2), [
                perm1, perm2,
            ])
        self.assertItemsEqual(backend.get_all_permissions(user3), [
                perm1, perm2, perm3,
            ])
        self.assertItemsEqual(backend.get_all_permissions(user4), [
                perm1, perm2, perm4, perm5,
            ])
        self.assertItemsEqual(backend.get_all_permissions(user5), [
                perm1, perm2, perm4, perm5,
            ])
        self.assertItemsEqual(backend.get_all_permissions(user6), [
                perm1, perm2, perm4, perm5, perm6,
            ])
        self.assertItemsEqual(backend.get_all_permissions(user7), [
                perm1, perm2, perm4, perm5, perm7,
            ])
        self.assertItemsEqual(backend.get_all_permissions(user8), [
                perm1, perm2, perm8,
            ])

    def test_has_role(self):
        backend = RoleBackend()

        user1, user2, user3, user4 = self.user1, self.user2, self.user3, self.user4
        user5, user6, user7, user8 = self.user5, self.user6, self.user7, self.user8

        self.assertTrue(backend.has_role(user1, 'permission_test_role1'))
        self.assertFalse(backend.has_role(user1, 'permission_test_role2'))
        self.assertFalse(backend.has_role(user1, 'permission_test_role3'))
        self.assertFalse(backend.has_role(user1, 'permission_test_role4'))
        self.assertFalse(backend.has_role(user1, 'permission_test_role5'))
        self.assertFalse(backend.has_role(user1, 'permission_test_role6'))

        self.assertTrue(backend.has_role(user2, 'permission_test_role1'))
        self.assertFalse(backend.has_role(user2, 'permission_test_role2'))
        self.assertFalse(backend.has_role(user2, 'permission_test_role3'))
        self.assertFalse(backend.has_role(user2, 'permission_test_role4'))
        self.assertFalse(backend.has_role(user2, 'permission_test_role5'))
        self.assertFalse(backend.has_role(user2, 'permission_test_role6'))

        self.assertTrue(backend.has_role(user3, 'permission_test_role1'))
        self.assertTrue(backend.has_role(user3, 'permission_test_role2'))
        self.assertFalse(backend.has_role(user3, 'permission_test_role3'))
        self.assertFalse(backend.has_role(user3, 'permission_test_role4'))
        self.assertFalse(backend.has_role(user3, 'permission_test_role5'))
        self.assertFalse(backend.has_role(user3, 'permission_test_role6'))

        self.assertTrue(backend.has_role(user4, 'permission_test_role1'))
        self.assertFalse(backend.has_role(user4, 'permission_test_role2'))
        self.assertTrue(backend.has_role(user4, 'permission_test_role3'))
        self.assertFalse(backend.has_role(user4, 'permission_test_role4'))
        self.assertFalse(backend.has_role(user4, 'permission_test_role5'))
        self.assertFalse(backend.has_role(user4, 'permission_test_role6'))

        self.assertTrue(backend.has_role(user5, 'permission_test_role1'))
        self.assertFalse(backend.has_role(user5, 'permission_test_role2'))
        self.assertTrue(backend.has_role(user5, 'permission_test_role3'))
        self.assertFalse(backend.has_role(user5, 'permission_test_role4'))
        self.assertFalse(backend.has_role(user5, 'permission_test_role5'))
        self.assertFalse(backend.has_role(user5, 'permission_test_role6'))

        self.assertTrue(backend.has_role(user6, 'permission_test_role1'))
        self.assertFalse(backend.has_role(user6, 'permission_test_role2'))
        self.assertTrue(backend.has_role(user6, 'permission_test_role3'))
        self.assertTrue(backend.has_role(user6, 'permission_test_role4'))
        self.assertFalse(backend.has_role(user6, 'permission_test_role5'))
        self.assertFalse(backend.has_role(user6, 'permission_test_role6'))

        self.assertTrue(backend.has_role(user7, 'permission_test_role1'))
        self.assertFalse(backend.has_role(user7, 'permission_test_role2'))
        self.assertTrue(backend.has_role(user7, 'permission_test_role3'))
        self.assertFalse(backend.has_role(user7, 'permission_test_role4'))
        self.assertTrue(backend.has_role(user7, 'permission_test_role5'))
        self.assertFalse(backend.has_role(user7, 'permission_test_role6'))

        self.assertTrue(backend.has_role(user8, 'permission_test_role1'))
        self.assertFalse(backend.has_role(user8, 'permission_test_role2'))
        self.assertFalse(backend.has_role(user8, 'permission_test_role3'))
        self.assertFalse(backend.has_role(user8, 'permission_test_role4'))
        self.assertFalse(backend.has_role(user8, 'permission_test_role5'))
        self.assertTrue(backend.has_role(user8, 'permission_test_role6'))
                                             
    def test_has_perm(self):
        backend = RoleBackend()

        user1, user2, user3, user4 = self.user1, self.user2, self.user3, self.user4
        user5, user6, user7, user8 = self.user5, self.user6, self.user7, self.user8

        self.assertTrue(backend.has_perm(user1, 'permission.permission_test_perm1'))
        self.assertTrue(backend.has_perm(user1, 'permission.permission_test_perm2'))
        self.assertFalse(backend.has_perm(user1, 'permission.permission_test_perm3'))
        self.assertFalse(backend.has_perm(user1, 'permission.permission_test_perm4'))
        self.assertFalse(backend.has_perm(user1, 'permission.permission_test_perm5'))
        self.assertFalse(backend.has_perm(user1, 'permission.permission_test_perm6'))
        self.assertFalse(backend.has_perm(user1, 'permission.permission_test_perm7'))
        self.assertFalse(backend.has_perm(user1, 'permission.permission_test_perm8'))
        
        self.assertTrue(backend.has_perm(user2, 'permission.permission_test_perm1'))
        self.assertTrue(backend.has_perm(user2, 'permission.permission_test_perm2'))
        self.assertFalse(backend.has_perm(user2, 'permission.permission_test_perm3'))
        self.assertFalse(backend.has_perm(user2, 'permission.permission_test_perm4'))
        self.assertFalse(backend.has_perm(user2, 'permission.permission_test_perm5'))
        self.assertFalse(backend.has_perm(user2, 'permission.permission_test_perm6'))
        self.assertFalse(backend.has_perm(user2, 'permission.permission_test_perm7'))
        self.assertFalse(backend.has_perm(user2, 'permission.permission_test_perm8'))
        
        self.assertTrue(backend.has_perm(user3, 'permission.permission_test_perm1'))
        self.assertTrue(backend.has_perm(user3, 'permission.permission_test_perm2'))
        self.assertTrue(backend.has_perm(user3, 'permission.permission_test_perm3'))
        self.assertFalse(backend.has_perm(user3, 'permission.permission_test_perm4'))
        self.assertFalse(backend.has_perm(user3, 'permission.permission_test_perm5'))
        self.assertFalse(backend.has_perm(user3, 'permission.permission_test_perm6'))
        self.assertFalse(backend.has_perm(user3, 'permission.permission_test_perm7'))
        self.assertFalse(backend.has_perm(user3, 'permission.permission_test_perm8'))
        
        self.assertTrue(backend.has_perm(user4, 'permission.permission_test_perm1'))
        self.assertTrue(backend.has_perm(user4, 'permission.permission_test_perm2'))
        self.assertFalse(backend.has_perm(user4, 'permission.permission_test_perm3'))
        self.assertTrue(backend.has_perm(user4, 'permission.permission_test_perm4'))
        self.assertTrue(backend.has_perm(user4, 'permission.permission_test_perm5'))
        self.assertFalse(backend.has_perm(user4, 'permission.permission_test_perm6'))
        self.assertFalse(backend.has_perm(user4, 'permission.permission_test_perm7'))
        self.assertFalse(backend.has_perm(user4, 'permission.permission_test_perm8'))
        
        self.assertTrue(backend.has_perm(user5, 'permission.permission_test_perm1'))
        self.assertTrue(backend.has_perm(user5, 'permission.permission_test_perm2'))
        self.assertFalse(backend.has_perm(user5, 'permission.permission_test_perm3'))
        self.assertTrue(backend.has_perm(user5, 'permission.permission_test_perm4'))
        self.assertTrue(backend.has_perm(user5, 'permission.permission_test_perm5'))
        self.assertFalse(backend.has_perm(user5, 'permission.permission_test_perm6'))
        self.assertFalse(backend.has_perm(user5, 'permission.permission_test_perm7'))
        self.assertFalse(backend.has_perm(user5, 'permission.permission_test_perm8'))
        
        self.assertTrue(backend.has_perm(user6, 'permission.permission_test_perm1'))
        self.assertTrue(backend.has_perm(user6, 'permission.permission_test_perm2'))
        self.assertFalse(backend.has_perm(user6, 'permission.permission_test_perm3'))
        self.assertTrue(backend.has_perm(user6, 'permission.permission_test_perm4'))
        self.assertTrue(backend.has_perm(user6, 'permission.permission_test_perm5'))
        self.assertTrue(backend.has_perm(user6, 'permission.permission_test_perm6'))
        self.assertFalse(backend.has_perm(user6, 'permission.permission_test_perm7'))
        self.assertFalse(backend.has_perm(user6, 'permission.permission_test_perm8'))
        
        self.assertTrue(backend.has_perm(user7, 'permission.permission_test_perm1'))
        self.assertTrue(backend.has_perm(user7, 'permission.permission_test_perm2'))
        self.assertFalse(backend.has_perm(user7, 'permission.permission_test_perm3'))
        self.assertTrue(backend.has_perm(user7, 'permission.permission_test_perm4'))
        self.assertTrue(backend.has_perm(user7, 'permission.permission_test_perm5'))
        self.assertFalse(backend.has_perm(user7, 'permission.permission_test_perm6'))
        self.assertTrue(backend.has_perm(user7, 'permission.permission_test_perm7'))
        self.assertFalse(backend.has_perm(user7, 'permission.permission_test_perm8'))
        
        self.assertTrue(backend.has_perm(user8, 'permission.permission_test_perm1'))
        self.assertTrue(backend.has_perm(user8, 'permission.permission_test_perm2'))
        self.assertFalse(backend.has_perm(user8, 'permission.permission_test_perm3'))
        self.assertFalse(backend.has_perm(user8, 'permission.permission_test_perm4'))
        self.assertFalse(backend.has_perm(user8, 'permission.permission_test_perm5'))
        self.assertFalse(backend.has_perm(user8, 'permission.permission_test_perm6'))
        self.assertFalse(backend.has_perm(user8, 'permission.permission_test_perm7'))
        self.assertTrue(backend.has_perm(user8, 'permission.permission_test_perm8'))

    def test_has_module_perm(self):
        backend = RoleBackend()

        user1 = self.user1

        self.assertTrue(backend.has_module_perms(user1, 'permission'))
        self.assertFalse(backend.has_module_perms(user1, 'auth'))

    def test_user_extension(self):
        from django.contrib.auth.models import User
        self.assertTrue(hasattr(User, 'has_role'))
        self.assertTrue(hasattr(User, 'roles'))
