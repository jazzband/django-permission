# django imports
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

import permissions.utils

class PermissionBase(object):
    """Mix-in class for permissions.
    """
    def grant_permission(self, role, permission):
        """Grants passed permission to passed role. Returns True if the
        permission was able to be added, otherwise False.

        **Parameters:**

        role
            The role for which the permission should be granted.

        permission
            The permission which should be granted. Either a permission
            object or the codename of a permission.
        """
        return permissions.utils.grant_permission(self, role, permission)

    def remove_permission(self, role, permission):
        """Removes passed permission from passed role. Returns True if the
        permission has been removed.

        **Parameters:**

        role
            The role for which a permission should be removed.

        permission
            The permission which should be removed. Either a permission object
            or the codename of a permission.
        """
        return permissions.utils.remove_permission(self, role, permission)

    def has_permission(self, user, permission, roles=[]):
        """Checks whether the passed user has passed permission for this
        instance.

        **Parameters:**

        permission
            The permission's codename which should be checked. Must be a
            string with a valid codename.

        user
            The user for which the permission should be checked.

        roles
            If passed, these roles will be assigned to the user temporarily
            before the permissions are checked.
        """
        return permissions.utils.has_permission(self, user, permission, roles)

    def add_inheritance_block(self, permission):
        """Adds an inheritance block for the passed permission.

        **Parameters:**

        permission
            The permission for which an inheritance block should be added.
            Either a permission object or the codename of a permission.
        """
        return permissions.utils.add_inheritance_block(self, permission)

    def remove_inheritance_block(self, permission):
        """Removes a inheritance block for the passed permission.

        **Parameters:**

        permission
            The permission for which an inheritance block should be removed.
            Either a permission object or the codename of a permission.
        """
        return permissions.utils.remove_inheritance_block(self, permission)

    def is_inherited(self, codename):
        """Returns True if the passed permission is inherited.

        **Parameters:**

        codename
            The permission which should be checked. Must be the codename of
            the permission.
        """
        return permissions.utils.is_inherited(self, codename)

    def add_role(self, principal, role):
        """Adds a local role for the principal.

        **Parameters:**

        principal
            The principal (user or group) which gets the role.

        role
            The role which is assigned.
        """
        return permissions.utils.add_local_role(self, principal, role)

    def get_roles(self, principal):
        """Returns local roles for passed principal (user or group).
        """
        return permissions.utils.get_local_roles(self, principal)

    def remove_role(self, principal, role):
        """Adds a local role for the principal to the object.

        **Parameters:**

        principal
            The principal (user or group) from which the role is removed.

        role
            The role which is removed.
        """
        return permissions.utils.remove_local_role(self, principal, role)

    def remove_roles(self, principal):
        """Removes all local roles for the passed principal from the object.

        **Parameters:**

        principal
            The principal (user or group) from which all local roles are
            removed.
        """
        return permissions.utils.remove_local_roles(self, principal)

class Permission(models.Model):
    """A permission which can be granted to users/groups and objects.

    **Attributes:**

    name
        The unique name of the permission. This is displayed to users.

    codename
        The unique codename of the permission. This is used internal to
        identify a permission.

    content_types
        The content types for which the permission is active. This can be
        used to display only reasonable permissions for an object.
    """
    name = models.CharField(_(u"Name"), max_length=100, unique=True)
    codename = models.CharField(_(u"Codename"), max_length=100, unique=True)
    content_types = models.ManyToManyField(ContentType, verbose_name=_(u"Content Types"), blank=True, null=True, related_name="content_types")

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.codename)

class ObjectPermission(models.Model):
    """Grants permission for specific user/group and object.

    **Attributes:**

    role
        The role for which the permission is granted.

    permission
        The permission which is granted.

    content
        The object for which the permission is granted.
    """
    role = models.ForeignKey("Role", verbose_name=_(u"Role"), blank=True, null=True)
    permission = models.ForeignKey(Permission, verbose_name=_(u"Permission"))

    content_type = models.ForeignKey(ContentType, verbose_name=_(u"Content type"))
    content_id = models.PositiveIntegerField(verbose_name=_(u"Content id"))
    content = generic.GenericForeignKey(ct_field="content_type", fk_field="content_id")

    def __unicode__(self):
        if self.role:
            principal = self.role
        else:
            principal = self.user

        return "%s / %s / %s - %s" % (self.permission.name, principal, self.content_type, self.content_id)

    def get_principal(self):
        """Returns the principal.
        """
        return self.user or self.group

    def set_principal(self, principal):
        """Sets the principal.
        """
        if isinstance(principal, User):
            self.user = principal
        else:
            self.group = principal

    principal = property(get_principal, set_principal)

class ObjectPermissionInheritanceBlock(models.Model):
    """Blocks the inheritance for specific permission and object.

    **Attributes:**

    permission
        The permission for which inheritance is blocked.

    content
        The object for which the inheritance is blocked.
    """
    permission = models.ForeignKey(Permission, verbose_name=_(u"Permission"))

    content_type = models.ForeignKey(ContentType, verbose_name=_(u"Content type"))
    content_id = models.PositiveIntegerField(verbose_name=_(u"Content id"))
    content = generic.GenericForeignKey(ct_field="content_type", fk_field="content_id")

    def __unicode__(self):
        return "%s / %s - %s" % (self.permission, self.content_type, self.content_id)

class Role(models.Model):
    """A role gets permissions to do something. Principals (users and groups)
    can only get permissions via roles.

    **Attributes:**

    name
        The unique name of the role
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name", )

    def __unicode__(self):
        return self.name

    def add_principal(self, principal, content=None):
        """
        """
        if isinstance(principal, User):
            PrincipalRoleRelation.objects.create(user=principal, role=self)
        else:
            PrincipalRoleRelation.objects.create(group=principal, role=self)

    def get_groups(self, content=None):
        """Returns all groups which has this role assigned.
        """
        return PrincipalRoleRelation.objects.filter(role=self, content=content)

    def get_users(self, content=None):
        """Returns all users which has this role assigned.
        """
        return PrincipalRoleRelation.objects.filter(role=self, content=content)

class PrincipalRoleRelation(models.Model):
    """A role given to a principal (user or group). If a content object is
    given this is a local role, i.e. the principal has this role only for this
    content object. Otherwise it is a global role, i.e. the principal has
    this role generally.

    user
        A user instance. Either a user xor a group needs to be given.

    group
        A group instance. Either a user xor a group needs to be given.

    role
        The role which is given to the principal for content.

    content
        The content object which gets the local role (optional).
    """
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    group = models.ForeignKey(Group, verbose_name=_(u"Group"), blank=True, null=True)
    role = models.ForeignKey(Role, verbose_name=_(u"Role"))

    content_type = models.ForeignKey(ContentType, verbose_name=_(u"Content type"), blank=True, null=True)
    content_id = models.PositiveIntegerField(verbose_name=_(u"Content id"), blank=True, null=True)
    content = generic.GenericForeignKey(ct_field="content_type", fk_field="content_id")

    def get_principal(self):
        """Returns the principal.
        """
        return self.user or self.group

    def set_principal(self, principal):
        """Sets the principal.
        """
        if isinstance(principal, User):
            self.user = principal
        else:
            self.group = principal

    principal = property(get_principal, set_principal)