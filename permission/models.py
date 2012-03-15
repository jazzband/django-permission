# vim: set fileencoding=utf-8 :
"""
Permission handler base


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
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from mptt.models import TreeManager

class RoleManager(TreeManager):
    def get_by_natural_key(self, codename):
        return self.get(codename=codename)

    def filter_by_user(self, user_obj):
        """return queryset of roles which ``user_obj`` have"""
        # do not defer anything otherwise the returning queryset
        # contains defered instance.
        roles_qs = self.none()
        for role in self.filter(_users=user_obj).iterator():
            roles_qs |= role.get_ancestors()
            roles_qs |= self.filter(pk=role.pk)
        return roles_qs

    def get_all_permissions_of_user(self, user_obj):
        """get a set of all permissions of ``user_obj``"""
        # name, parent, _users, _permissions are required.
        roles = self.defer('codename', 'description').filter(_users=user_obj)
        permissions = Permission.objects.none()
        for role in roles.iterator():
            permissions |= role.permissions
        return permissions.distinct()


class Role(MPTTModel):
    """A role model for enhanced permission system."""
    name = models.CharField(_('name'), max_length=50)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True,
            help_text=_('A description of this permission role'))

    parent = TreeForeignKey('self', verbose_name=_('parent role'),
            related_name='children', blank=True, null=True)

    _users = models.ManyToManyField(User, verbose_name=_('user'),
            related_name='_roles', db_column='users', blank=True)

    _permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'),
            related_name='roles', db_column='permissions', blank=True)

    objects = RoleManager()

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.codename,)

    @property
    def users(self):
        """get all users who belongs to this role or superroles"""
        role_pks = self.get_descendants(True).values_list('id', flat=True)
        qs = User.objects.only('id', '_roles').filter(_roles__pk__in=role_pks).distinct()
        qs = qs.defer(None)
        def remove_role_perm_cache_before(fn):
            def inner(manager, *objs):
                for obj in objs:
                    if hasattr(obj, '_role_perm_cache'):
                        delattr(obj, '_role_perm_cache')
                return fn(manager, *objs)
            return inner
        # add methods
        qs.add = remove_role_perm_cache_before(self._users.add)
        qs.remove = remove_role_perm_cache_before(self._users.remove)
        qs.clear = self._users.clear
        return qs

    @property
    def permissions(self):
        """get all permissions which this role or subroles have"""
        role_pks = list(self.get_ancestors().values_list('id', flat=True))
        role_pks.append(self.pk)
        qs = Permission.objects.only('id', 'roles').filter(roles__pk__in=role_pks).distinct()
        qs = qs.defer(None)
        # add methods
        qs.add = self._permissions.add
        qs.remove = self._permissions.remove
        qs.clear = self._permissions.clear
        return qs

    def is_belong(self, user_obj):
        """whether the ``user_obj`` belongs to this role or superroles"""
        return self.users.filter(pk=user_obj.pk).exists()


def get_permission_instance(str_or_instance):
    """get permission instance from string or instance"""
    if isinstance(str_or_instance, basestring):
        app_label, codename = str_or_instance.split('.', 1)
        instance = Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename
            )
    else:
        instance = str_or_instance
    return instance
