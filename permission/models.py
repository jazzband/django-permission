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


class RoleManager(models.Manager):
    def get_by_natural_key(self, codename):
        return self.get(codename=codename)

    def filter_by_user(self, user_obj):
        """return queryset of roles which ``user_obj`` have"""
        roles_qs = self.defer('id', '_users').filter(_users=user_obj)
        roles = []
        for role in roles_qs.iterator():
            roles.extend(role.roles)
        role_pks = [r.pk for r in set(roles)]
        roles = self.defer('id').filter(pk__in=role_pks)
        return roles.defer(None)

    def get_all_permissions_of_user(self, user_obj):
        """get a set of all permissions of ``user_obj``"""
        roles = self.defer('id', '_users').filter(_users=user_obj)
        permissions = []
        for role in roles.iterator():
            permissions.extend(role.permissions)
        return frozenset(permissions)


class Role(models.Model):
    """A role model for enhanced permission system."""
    name = models.CharField(_('name'), max_length=50)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True,
            help_text=_('A description of this permission role'))

    _subroles = models.ManyToManyField('self', verbose_name=_('sub roles'),
            related_name='_superroles', db_column='subroles', symmetrical=False, blank=True)

    _users = models.ManyToManyField(User, verbose_name=_('user'),
            related_name='_roles', db_column='users', blank=True)

    _permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'),
            related_name='roles', db_column='permissions', blank=True)

    objects = RoleManager()

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __unicode__(self):
        return u"<Role: %s>" % self.codename

    def natural_key(self):
        return (self.codename,)

    def _get_all_subroles(self):
        """get a frozenset of all subroles of this role"""
        roles = []
        for role in self._subroles.iterator():
            roles.append(role)
            roles.extend(role._get_all_subroles())
        return frozenset(roles)
    subroles = property(_get_all_subroles)

    def _get_all_roles(self):
        """get a frozenset of all subroles and this role"""
        roles = set(self.subroles)
        roles.add(self)
        return frozenset(roles)
    roles = property(_get_all_roles)

    def _get_all_users(self):
        """get all users who belongs to this role or superroles"""
        role_pks = [r.pk for r in self.roles]
        qs = User.objects.defer('pk', '_roles').filter(_roles__pk__in=role_pks).distinct()
        return qs.defer(None)
    users = property(_get_all_users)

    def _get_all_permissions(self):
        """get all permissions which this role or subroles have"""
        role_pks = [r.pk for r in self.roles]
        qs = Permission.objects.defer('pk', 'roles').filter(roles__pk__in=role_pks).distinct()
        return qs.defer(None)
    permissions = property(_get_all_permissions)

    def is_belong(self, user_obj):
        """whether the ``user_obj`` belongs to this role or superroles"""
        return self.users.filter(pk=user_obj.pk).exists()

    def add_users(self, *user_or_iterable):
        """add users if the users have not belong to this role or subroles
        
        .. Note::
            Adding user doesn't add the user who belongs to this role or
            all subroles of this role. Adding users directly to ``_users``
            is not recommended.

        """
        if isinstance(user_or_iterable, User):
            user_or_iterable = [user_or_iterable]
        user_or_iterable = frozenset(user_or_iterable)
        existing_users = frozenset(self.users.all())
        user_or_iterable = user_or_iterable.difference(existing_users)
        if len(user_or_iterable) > 0:
            self._users.add(*user_or_iterable)

    def remove_users(self, *user_or_iterable):
        """remove users if the users have belong to this role
        
        .. Note::
            Removing user doesn't remove the user who have not belong to this
            role. All users who belongs to the subroles of this roles are
            protected from removing by ``remove_users``.

        """
        if isinstance(user_or_iterable, User):
            user_or_iterable = [user_or_iterable]
        user_or_iterable = frozenset(user_or_iterable)
        existing_users = frozenset(self._users.all())
        user_or_iterable = user_or_iterable.intersection(existing_users)
        if len(user_or_iterable) > 0:
            self._users.remove(*user_or_iterable)

    def add_permissions(self, *perm_or_iterable):
        """add permissions if the permissions have not belong to this role or subroles
        
        .. Note::
            Adding permissions doesn't add the permission which belongs to this role or
            all subroles of this role. Adding permissions directly to ``_permissions``
            is not recommended.

        """
        if isinstance(perm_or_iterable, (basestring, Permission)):
            perm_or_iterable = [perm_or_iterable]
        existing_perms = self.permissions
        for perm in perm_or_iterable:
            if isinstance(perm, basestring):
                app_label, codename = perm.split('.', 1)
                instance = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
            else:
                instance = perm
                app_label = perm.content_type.app_label
                codename = perm.codename
            if not existing_perms.filter(content_type__app_label=app_label, codename=codename).exists():
                self._permissions.add(instance)

    def remove_permissions(self, *perm_or_iterable):
        """remove permissions if the permissions have belong to this role
        
        .. Note::
            Removing permission doesn't remove the permission who have not belong to this
            role. All permissions who belongs to the subroles of this roles are
            protected from removing by ``remove_permissions``.

        """
        if isinstance(perm_or_iterable, (basestring, Permission)):
            perm_or_iterable = [perm_or_iterable]
        existing_perms = self.permissions
        for perm in perm_or_iterable:
            if isinstance(perm, basestring):
                app_label, codename = perm.split('.', 1)
                instance = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
            else:
                instance = perm
                app_label = perm.content_type.app_label
                codename = perm.codename
            if existing_perms.filter(content_type__app_label=app_label, codename=codename).exists():
                self._permissions.remove(instance)

