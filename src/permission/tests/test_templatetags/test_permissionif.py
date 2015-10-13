# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.template import Context
from django.template import Template

from permission.tests.utils import create_user
from permission.tests.utils import create_article
from permission.tests.utils import create_permission
from permission.tests.compatibility import override_settings
from permission.utils.handlers import registry


@override_settings(
    AUTHENTICATION_BACKENDS=(
        'django.contrib.auth.backends.ModelBackend',
        'permission.backends.PermissionBackend',
    ),
    PERMISSION_REPLACE_BUILTIN_IF=False,
)
class PermissionTemplateTagsTestCase(TestCase):

    def setUp(self):
        # store original registry
        self._original_registry = registry._registry
        # clear registry and register mock handler
        registry._registry = {}

    def tearDown(self):
        # restore original reigstry
        registry._registry = self._original_registry

    def test_permissionif_tag(self):
        user = create_user('permission_templatetag_test_user1')
        perm = create_permission('permission_templatetag_test_perm1')

        user.user_permissions.add(perm)

        self.assertTrue(user.has_perm(
            'permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% load permissionif %}"
            "{% permission user has "
            "'permission.permission_templatetag_test_perm1' %}"
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

        self.assertTrue(user.has_perm(
            'permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% load permissionif %}"
            "{% permission user has 'permission.unknown_permission' %}"
            "Fail"
            "{% elpermission user has 'permission.unknown_permisson2' %}"
            "Fail"
            "{% elpermission user has "
            "'permission.permission_templatetag_test_perm1' %}"
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

        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% load permissionif %}"
            "{% permission user has 'permission.unknown_permission' %}"
            "Fail"
            "{% else %}"
            "Success"
            "{% endpermission %}"
        ).render(context)

        self.assertEqual(out, "Success")

    def test_permissionif_tag_with_obj(self):
        from permission.tests.models import Article
        from permission.handlers import PermissionHandler

        user = create_user('permission_templatetag_test_user1')
        art1 = create_article('permission_templatetag_test_article1')
        art2 = create_article('permission_templatetag_test_article2')
        create_permission('permission_templatetag_test_perm1')

        class ArticlePermissionHandler(PermissionHandler):

            def has_perm(self, user_obj, perm, obj=None):
                if perm == 'permission.permission_templatetag_test_perm1':
                    if (obj and obj.title ==
                            'permission_templatetag_test_article2'):
                        return True
                return False
        registry.register(Article, ArticlePermissionHandler)

        self.assertFalse(
            user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertFalse(
            user.has_perm('permission.permission_templatetag_test_perm1',
                          art1))
        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1',
                          art2))

        context = Context({
            'user': user,
            'art1': art1,
            'art2': art2,
        })

        out = Template(
            "{% load permissionif %}"
            "{% permission user has "
            "'permission.permission_templatetag_test_perm1' %}"
            "Fail"
            "{% elpermission user has "
            "'permission.permission_templatetag_test_perm1' of art1 %}"
            "Fail"
            "{% elpermission user has "
            "'permission.permission_templatetag_test_perm1' of art2 %}"
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

        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm2'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% load permissionif %}"
            "{% permission user has 'permission.unknown_perm' "
            "and user has 'permission.permission_templatetag_test_perm2' %}"
            "Fail"
            "{% elpermission user has "
            "'permission.permission_templatetag_test_perm1' "
            "and user has 'permission.unknown_perm' %}"
            "Fail"
            "{% elpermission user has "
            "'permission.permission_templatetag_test_perm1' "
            "and user has 'permission.permission_templatetag_test_perm2' %}"
            "Success"
            "{% endpermission %}"
        ).render(context)

        self.assertEqual(out, "Success")

    def test_permissionif_tag_or(self):

        user = create_user('permission_templatetag_test_user1')
        perm1 = create_permission('permission_templatetag_test_perm1')
        create_permission('permission_templatetag_test_perm2')

        user.user_permissions.add(perm1)

        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertFalse(
            user.has_perm('permission.permission_templatetag_test_perm2'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% load permissionif %}"
            "{% permission user has "
            "'permission.permission_templatetag_test_perm1' "
            "and user has 'permission.permission_templatetag_test_perm2' %}"
            "Fail"
            "{% elpermission user has "
            "'permission.permission_templatetag_test_perm1' "
            "or user has 'permission.permission_templatetag_test_perm2' %}"
            "Success"
            "{% endpermission %}"
        ).render(context)

        self.assertEqual(out, "Success")


@override_settings(
    AUTHENTICATION_BACKENDS=(
        'django.contrib.auth.backends.ModelBackend',
        'permission.backends.PermissionBackend',
    ),
    PERMISSION_REPLACE_BUILTIN_IF=True,
)
class PermissionTemplateTagsWithBuiltinTestCase(TestCase):

    def setUp(self):
        # store original registry
        self._original_registry = registry._registry
        # clear registry and register mock handler
        registry._registry = {}

    def tearDown(self):
        # restore original reigstry
        registry._registry = self._original_registry

    def test_if_tag(self):
        user = create_user('permission_templatetag_test_user1')
        perm = create_permission('permission_templatetag_test_perm1')

        user.user_permissions.add(perm)

        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% if user has 'permission.permission_templatetag_test_perm1' %}"
            "Success"
            "{% else %}"
            "Fail"
            "{% endif %}"
        ).render(context)

        self.assertEqual(out, "Success")

    def test_if_tag_elif(self):
        user = create_user('permission_templatetag_test_user1')
        perm = create_permission('permission_templatetag_test_perm1')

        user.user_permissions.add(perm)

        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% if user has 'permission.unknown_permission' %}"
            "Fail"
            "{% elif user has 'permission.unknown_permisson2' %}"
            "Fail"
            "{% elif user has "
            "'permission.permission_templatetag_test_perm1' %}"
            "Success"
            "{% else %}"
            "Fail"
            "{% endif %}"
        ).render(context)

        self.assertEqual(out, "Success")

    def test_if_tag_else(self):
        user = create_user('permission_templatetag_test_user1')
        perm = create_permission('permission_templatetag_test_perm1')

        user.user_permissions.add(perm)

        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% if user has 'permission.unknown_permission' %}"
            "Fail"
            "{% else %}"
            "Success"
            "{% endif %}"
        ).render(context)

        self.assertEqual(out, "Success")

    def test_if_tag_with_obj(self):
        from permission.tests.models import Article
        from permission.handlers import PermissionHandler

        user = create_user('permission_templatetag_test_user1')
        art1 = create_article('permission_templatetag_test_article1')
        art2 = create_article('permission_templatetag_test_article2')
        create_permission('permission_templatetag_test_perm1')

        class ArticlePermissionHandler(PermissionHandler):
            def has_perm(self, user_obj, perm, obj=None):
                if perm == 'permission.permission_templatetag_test_perm1':
                    if (obj and obj.title ==
                            'permission_templatetag_test_article2'):
                        return True
                return False
        registry.register(Article, ArticlePermissionHandler)

        self.assertFalse(
            user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertFalse(
            user.has_perm('permission.permission_templatetag_test_perm1',
                          art1))
        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1',
                          art2))

        context = Context({
            'user': user,
            'art1': art1,
            'art2': art2,
        })

        out = Template(
            "{% if user has 'permission.permission_templatetag_test_perm1' %}"
            "Fail"
            "{% elif user has "
            "'permission.permission_templatetag_test_perm1' of art1 %}"
            "Fail"
            "{% elif user has "
            "'permission.permission_templatetag_test_perm1' of art2 %}"
            "Success"
            "{% else %}"
            "Fail"
            "{% endif %}"
        ).render(context)

        self.assertEqual(out, "Success")

    def test_if_tag_and(self):
        user = create_user('permission_templatetag_test_user1')
        perm1 = create_permission('permission_templatetag_test_perm1')
        perm2 = create_permission('permission_templatetag_test_perm2')

        user.user_permissions.add(perm1, perm2)

        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm2'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% if user has 'permission.unknown_perm' "
            "and user has 'permission.permission_templatetag_test_perm2' %}"
            "Fail"
            "{% elif user has 'permission.permission_templatetag_test_perm1' "
            "and user has 'permission.unknown_perm' %}"
            "Fail"
            "{% elif user has 'permission.permission_templatetag_test_perm1' "
            "and user has 'permission.permission_templatetag_test_perm2' %}"
            "Success"
            "{% endif %}"
        ).render(context)

        self.assertEqual(out, "Success")

    def test_if_tag_or(self):

        user = create_user('permission_templatetag_test_user1')
        perm1 = create_permission('permission_templatetag_test_perm1')
        create_permission('permission_templatetag_test_perm2')

        user.user_permissions.add(perm1)

        self.assertTrue(
            user.has_perm('permission.permission_templatetag_test_perm1'))
        self.assertFalse(
            user.has_perm('permission.permission_templatetag_test_perm2'))

        context = Context({
            'user': user,
        })

        out = Template(
            "{% if user has 'permission.permission_templatetag_test_perm1' "
            "and user has 'permission.permission_templatetag_test_perm2' %}"
            "Fail"
            "{% elif user has 'permission.permission_templatetag_test_perm1' "
            "or user has 'permission.permission_templatetag_test_perm2' %}"
            "Success"
            "{% endif %}"
        ).render(context)

        self.assertEqual(out, "Success")
