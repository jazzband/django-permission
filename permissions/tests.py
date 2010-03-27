# django imports
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

# permissions imports
from permissions.models import Permission
from permissions.models import ObjectPermission
from permissions.models import ObjectPermissionInheritanceBlock
from permissions.models import Role

import permissions.utils

class RoleTestCase(TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.role_1 = permissions.utils.register_role("Role 1")
        self.role_2 = permissions.utils.register_role("Role 2")

        self.user = User.objects.create(username="john")

        self.page_1 = FlatPage.objects.create(url="/page-1/", title="Page 1")
        self.page_2 = FlatPage.objects.create(url="/page-1/", title="Page 2")

    def test_global_roles(self):
        """
        """
        # Add role 1    
        result = permissions.utils.add_role(self.user, self.role_1)
        self.assertEqual(result, True)

        # Add role 1 again
        result = permissions.utils.add_role(self.user, self.role_1)
        self.assertEqual(result, False)

        result = permissions.utils.get_roles(self.user)
        self.assertEqual(result, [self.role_1])

        # Add role 2
        result = permissions.utils.add_role(self.user, self.role_2)
        self.assertEqual(result, True)

        result = permissions.utils.get_roles(self.user)
        self.assertEqual(result, [self.role_1, self.role_2])
        
        # Remove role 1
        result = permissions.utils.remove_role(self.user, self.role_1)
        self.assertEqual(result, True)

        # Remove role 1 again
        result = permissions.utils.remove_role(self.user, self.role_1)
        self.assertEqual(result, False)

        result = permissions.utils.get_roles(self.user)
        self.assertEqual(result, [self.role_2])

        # Remove role 2
        result = permissions.utils.remove_role(self.user, self.role_2)
        self.assertEqual(result, True)

        result = permissions.utils.get_roles(self.user)
        self.assertEqual(result, [])

class PermissionTestCase(TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.role_1 = permissions.utils.register_role("Role 1")
        self.role_2 = permissions.utils.register_role("Role 2")

        self.user = User.objects.create(username="john")
        permissions.utils.add_role(self.user, self.role_1)
        self.user.save()

        self.page_1 = FlatPage.objects.create(url="/page-1/", title="Page 1")
        self.page_2 = FlatPage.objects.create(url="/page-1/", title="Page 2")

        self.permission = permissions.utils.register_permission("View", "view")

    def test_has_permission_role(self):
        """
        """
        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, False)

        result = permissions.utils.grant_permission(self.page_1, self.permission, self.role_1)
        self.assertEqual(result, True)

        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, True)

        result = permissions.utils.remove_permission(self.page_1, "view", self.role_1)
        self.assertEqual(result, True)

        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, False)

    def test_has_permission_owner(self):
        """
        """
        creator = User.objects.create(username="jane")

        result = permissions.utils.has_permission(self.page_1, "view", creator)
        self.assertEqual(result, False)

        owner = permissions.utils.register_role("Owner")
        permissions.utils.grant_permission(self.page_1, "view", owner)

        result = permissions.utils.has_permission(self.page_1, "view", creator, [owner])
        self.assertEqual(result, True)

    def test_local_role(self):
        """
        """
        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, False)

        permissions.utils.grant_permission(self.page_1, self.permission, self.role_2)
        permissions.utils.add_local_role(self.page_1, self.user, self.role_2)

        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, True)

    def test_ineritance(self):
        """
        """
        result = permissions.utils.is_inherited(self.page_1, "view")
        self.assertEqual(result, True)

        permissions.utils.add_inheritance_block(self.page_1, self.permission)

        result = permissions.utils.is_inherited(self.page_1, "view")
        self.assertEqual(result, False)

    def test_unicode(self):
        """
        """
        # Permission
        self.assertEqual(self.permission.__unicode__(), "View (view)")

        # ObjectPermission
        permissions.utils.grant_permission(self.page_1, self.permission, self.role_1)
        opr = ObjectPermission.objects.get(permission=self.permission, role=self.role_1)
        self.assertEqual(opr.__unicode__(), "View / Role 1 / flat page - 1")

        # ObjectPermissionInheritanceBlock
        permissions.utils.add_inheritance_block(self.page_1, self.permission)
        opb = ObjectPermissionInheritanceBlock.objects.get(permission=self.permission)

        self.assertEqual(opb.__unicode__(), "View (view) / flat page - 1")

class RegistrationTestCase(TestCase):
    """Tests the registration of different components.
    """
    def test_role(self):
        """Tests registering/unregistering of a role.
        """
        # Register a role
        result = permissions.utils.register_role("Editor")
        self.failUnless(isinstance(result, Role))

        # It's there
        role = Role.objects.get(name="Editor")
        self.assertEqual(role.name, "Editor")

        # Trying to register another role with same name
        result = permissions.utils.register_role("Editor")
        self.assertEqual(result, False)

        role = Role.objects.get(name="Editor")
        self.assertEqual(role.name, "Editor")

        # Unregister the role
        result = permissions.utils.unregister_role("Editor")
        self.assertEqual(result, True)

        # It's not there anymore
        self.assertRaises(Role.DoesNotExist, Role.objects.get, name="Editor")

        # Trying to unregister the role again
        result = permissions.utils.unregister_role("Editor")
        self.assertEqual(result, False)

    def test_permission(self):
        """Tests registering/unregistering of a permission.
        """
        # Register a permission
        result = permissions.utils.register_permission("Change", "change")
        self.failUnless(isinstance(result, Permission))

        # Is it there?
        p = Permission.objects.get(codename="change")
        self.assertEqual(p.name, "Change")

        # Register a permission with the same codename
        result = permissions.utils.register_permission("Change2", "change")
        self.assertEqual(result, False)

        # Is it there?
        p = Permission.objects.get(codename="change")
        self.assertEqual(p.name, "Change")

        # Register a permission with the same name
        result = permissions.utils.register_permission("Change", "change2")
        self.assertEqual(result, False)

        # Is it there?
        p = Permission.objects.get(codename="change")
        self.assertEqual(p.name, "Change")

        # Unregister the permission
        result = permissions.utils.unregister_permission("change")
        self.assertEqual(result, True)

        # Is it not there anymore?
        self.assertRaises(Permission.DoesNotExist, Permission.objects.get, codename="change")

        # Unregister the permission again
        result = permissions.utils.unregister_permission("change")
        self.assertEqual(result, False)

# django imports
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import User
from django.contrib.sessions.backends.file import SessionStore
from django.test.client import Client

# Taken from "http://www.djangosnippets.org/snippets/963/"
class RequestFactory(Client):
    """
    Class that lets you create mock Request objects for use in testing.

    Usage:

    rf = RequestFactory()
    get_request = rf.get('/hello/')
    post_request = rf.post('/submit/', {'foo': 'bar'})

    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client

    Once you have a request object you can pass it to any view function,
    just as if that view had been hooked up using a URLconf.

    """
    def request(self, **request):
        """
        Similar to parent class, but returns the request object as soon as it
        has created it.
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)

def create_request():
    """
    """
    rf = RequestFactory()
    request = rf.get('/')
    request.session = SessionStore()

    user = User()
    user.is_superuser = True
    user.save()
    request.user = user

    return request