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
import permissions.utils

class PermissionTestCase(TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.group_1 = permissions.utils.register_group("Group 1")
        self.group_2 = permissions.utils.register_group("Group 2")

        self.user = User.objects.create(username="john")
        self.user.groups.add(self.group_1)
        self.user.groups.add(self.group_2)
        self.user.save()

        self.page_1 = FlatPage.objects.create(url="/page-1/", title="Page 1")
        self.page_2 = FlatPage.objects.create(url="/page-1/", title="Page 2")

        self.permission = permissions.utils.register_permission("View", "view")

    def test_has_permission_group(self):
        """
        """
        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, False)

        result = permissions.utils.grant_permission(self.page_1, self.permission, self.group_1)
        self.assertEqual(result, True)

        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, True)

        result = permissions.utils.remove_permission(self.page_1, "view", self.group_1)
        self.assertEqual(result, True)

        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, False)

    def test_has_permission_owner(self):
        """
        """
        creator = User.objects.create(username="jane")

        result = permissions.utils.has_permission(self.page_1, "view", creator)
        self.assertEqual(result, False)

        owner = permissions.utils.register_group("Owner")
        permissions.utils.grant_permission(self.page_1, "view", owner)

        result = permissions.utils.has_permission(self.page_1, "view", creator, [owner])
        self.assertEqual(result, True)

    def test_has_permission_user(self):
        """
        """
        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, False)

        result = permissions.utils.grant_permission(self.page_1, self.permission, self.user)
        self.assertEqual(result, True)

        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, True)

        result = permissions.utils.remove_permission(self.page_1, "view", self.user)
        self.assertEqual(result, True)

        result = permissions.utils.has_permission(self.page_1, "view", self.user)
        self.assertEqual(result, False)

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
        permissions.utils.grant_permission(self.page_1, self.permission, self.group_1)
        opr = ObjectPermission.objects.get(permission=self.permission, group=self.group_1)
        self.assertEqual(opr.__unicode__(), "View / Group 1 / flat page - 1")

        permissions.utils.grant_permission(self.page_1, self.permission, self.user)
        opr = ObjectPermission.objects.get(permission=self.permission, user=self.user)
        self.assertEqual(opr.__unicode__(), "View / john / flat page - 1")

        # ObjectPermissionInheritanceBlock
        permissions.utils.add_inheritance_block(self.page_1, self.permission)
        opb = ObjectPermissionInheritanceBlock.objects.get(permission=self.permission)

        self.assertEqual(opb.__unicode__(), "View (view) / flat page - 1")

class RegistrationTestCase(TestCase):
    """Tests the registration of different components.
    """
    def test_group(self):
        """Tests registering/unregistering of a group.
        """
        # Register a group
        result = permissions.utils.register_group("Brights")
        self.failUnless(isinstance(result, Group))

        # It's there
        group = Group.objects.get(name="Brights")
        self.assertEqual(group.name, "Brights")

        # Trying to register another group with same name
        result = permissions.utils.register_group("Brights")
        self.assertEqual(result, False)

        group = Group.objects.get(name="Brights")
        self.assertEqual(group.name, "Brights")

        # Unregister the group
        result = permissions.utils.unregister_group("Brights")
        self.assertEqual(result, True)

        # It's not there anymore
        self.assertRaises(Group.DoesNotExist, Group.objects.get, name="Brights")

        # Trying to unregister the group again
        result = permissions.utils.unregister_group("Brights")
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