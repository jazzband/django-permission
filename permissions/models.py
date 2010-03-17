# django imports
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

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

        group
            The group for which the permission is granted. Either this xor the
            user must be given.
        user
            The user for which the permission is granted. Either this xor the
            user must be given.
        permission
            The permission which is granted.
        content
            The object for which the permission is granted.
    """
    group = models.ForeignKey(Group, verbose_name=_(u"Group"), blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    permission = models.ForeignKey(Permission, verbose_name=_(u"Permission"))

    content_type = models.ForeignKey(ContentType, verbose_name=_(u"Content type"))
    content_id = models.PositiveIntegerField(verbose_name=_(u"Content id"))
    content = generic.GenericForeignKey(ct_field="content_type", fk_field="content_id")

    def __unicode__(self):
        if self.group:
            principal = self.group
        else:
            principal = self.user

        return "%s / %s / %s - %s" % (self.permission.name, principal, self.content_type, self.content_id)

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
