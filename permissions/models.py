# django imports
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

class PermissionBase(models.Model):
    """Mix-in class for permissions.
    """
    def add_role(self, principal, role):
        """Adds a local role for the principal to the object.
        """
        permissions.utils.add_role(principal, role, self)

    def remove_roles(self, principal):
        """Removes all local roles for the passed principal from the object.
        """
        permissions.utils.remove_roles(principal, role, self)

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
    """A role getting permissions for content objects. A role is the only way
    to grant permissions to user and groups.

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
    """A role given to a principal user or group. If a content object is passed
    this is a local role only for the given content object. Otherwise it is
    a global role.

    user
        A user instance. Either a user xor a group needs to be given.

    group
        A group instance. Either a user xor a group needs to be given.

    role
        The role which is given to the principal for content.

    content
        The content object which gets the local role.
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