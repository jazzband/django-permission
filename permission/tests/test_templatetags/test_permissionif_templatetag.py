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
from django.template import Context
from django.template import Template
from django.template import TemplateSyntaxError
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

from permission.tests.utils import create_user
from permission.tests.utils import create_role
from permission.tests.utils import create_permission

class PermissionTemplateTagsTestCase(TestCase):

    def test_permissionif_tag(self):
        user = create_user('permission_templatetag_test_user1')
        perm = create_permission('permission_templatetag_test_perm1')

        user.user_permissions.add(perm)

        self.assertTrue(user.has_perm('permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
                "{% load permission_tags %}"
                "{% permission user has 'permission.permission_templatetag_test_perm1' %}"
                "Success"
                "{% else %}"
                "Fail"
                "{% endpermission %}"
            ).render(context)

        self.assertEqual(out, "Success")
        

    def test_permissionif_tag_elif(self):
        user = create_user('permission_templatetag_test_user1')
        perm = create_permission('permission_templatetag_test_perm1')

        user.user_permissions.add(perm)

        self.assertTrue(user.has_perm('permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
                "{% load permission_tags %}"
                "{% permission user has 'permission.unknown_permission' %}"
                "Fail"
                "{% elpermission user has 'permission.unknown_permisson2' %}"
                "Fail"
                "{% elpermission user has 'permission.permission_templatetag_test_perm1' %}"
                "Success"
                "{% else %}"
                "Fail"
                "{% endpermission %}"
            ).render(context)

        self.assertEqual(out, "Success")
        
    def test_permissionif_tag_else(self):
        user = create_user('permission_templatetag_test_user1')
        perm = create_permission('permission_templatetag_test_perm1')

        user.user_permissions.add(perm)

        self.assertTrue(user.has_perm('permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
                "{% load permission_tags %}"
                "{% permission user has 'permission.unknown_permission' %}"
                "Fail"
                "{% else %}"
                "Success"
                "{% endpermission %}"
            ).render(context)

        self.assertEqual(out, "Success")
        

    def test_permissionif_tag_with_obj(self):
        from permission import registry
        from permission import PermissionHandler
        from permission.models import Role

        user = create_user('permission_templatetag_test_user1')
        role1 = create_role('permission_templatetag_test_role1')
        role2 = create_role('permission_templatetag_test_role2')
        perm = create_permission('permission_templatetag_test_perm1')

        class RolePermissionHandler(PermissionHandler):
            def has_perm(self, user_obj, perm, obj=None):
                if perm == 'permission.permission_templatetag_test_perm1':
                    if obj and obj.codename == 'permission_templatetag_test_role2':
                        return True
                return False
        registry.register(Role, RolePermissionHandler)

        self.assertFalse(user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertFalse(user.has_perm('permission.permission_templatetag_test_perm1', role1))
        self.assertTrue(user.has_perm('permission.permission_templatetag_test_perm1', role2))

        context = Context({
            'user': user,
            'role1': role1,
            'role2': role2,
        })

        out = Template(
                "{% load permission_tags %}"
                "{% permission user has 'permission.permission_templatetag_test_perm1' %}"
                "Fail"
                "{% elpermission user has 'permission.permission_templatetag_test_perm1' of role1 %}"
                "Fail"
                "{% elpermission user has 'permission.permission_templatetag_test_perm1' of role2 %}"
                "Success"
                "{% else %}"
                "Fail"
                "{% endpermission %}"
            ).render(context)

        self.assertEqual(out, "Success")

    def test_permissionif_tag_and(self):
        user = create_user('permission_templatetag_test_user1')
        perm1 = create_permission('permission_templatetag_test_perm1')
        perm2 = create_permission('permission_templatetag_test_perm2')

        user.user_permissions.add(perm1, perm2)

        self.assertTrue(user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertTrue(user.has_perm('permission.permission_templatetag_test_perm2'))

        context = Context({
            'user': user,
        })

        out = Template(
                "{% load permission_tags %}"
                "{% permission user has 'permission.unknown_perm' "
                "and user has 'permission.permission_templatetag_test_perm2' %}"
                "Fail"
                "{% elpermission user has 'permission.permission_templatetag_test_perm1' "
                "and user has 'permission.unknown_perm' %}"
                "Fail"
                "{% elpermission user has 'permission.permission_templatetag_test_perm1' "
                "and user has 'permission.permission_templatetag_test_perm2' %}"
                "Success"
                "{% endpermission %}"
            ).render(context)

        self.assertEqual(out, "Success")

    def test_permissionif_tag_or(self):

        user = create_user('permission_templatetag_test_user1')
        perm1 = create_permission('permission_templatetag_test_perm1')
        perm2 = create_permission('permission_templatetag_test_perm2')

        user.user_permissions.add(perm1)

        self.assertTrue(user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertFalse(user.has_perm('permission.permission_templatetag_test_perm2'))

        context = Context({
            'user': user,
        })

        out = Template(
                "{% load permission_tags %}"
                "{% permission user has 'permission.permission_templatetag_test_perm1' "
                "and user has 'permission.permission_templatetag_test_perm2' %}"
                "Fail"
                "{% elpermission user has 'permission.permission_templatetag_test_perm1' "
                "or user has 'permission.permission_templatetag_test_perm2' %}"
                "Success"
                "{% endpermission %}"
            ).render(context)

        self.assertEqual(out, "Success")
