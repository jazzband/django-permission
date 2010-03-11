# django imports
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

# permissions imports
from permissions.models import ObjectPermission
from permissions.models import ObjectPermissionInheritanceBlock
from permissions.models import Permission

# Permission #################################################################

def grant_permission(permission, group, obj):
    """Adds passed permission to passed group and object. Returns True if the
    permission was able to be added, otherwise False.

    **Parameters:**

        permission
            The permission for which should be removed. Either a permission 
            object or the codename of a permission.
        obj
            The content object for which an inheritance should be added.
    """
    if not isinstance(permission, Permission):
        try:
            permission = Permission.objects.get(codename = permission)
        except Permission.DoesNotExist:
            return False
    
    ct = ContentType.objects.get_for_model(obj)
    try:
        ObjectPermission.objects.get(group=group, content_type = ct, content_id=obj.id, permission=permission)
    except ObjectPermission.DoesNotExist:
        try:
            result = ObjectPermission.objects.create(group=group, content=obj, permission=permission)
        except IntegrityError:
            return False
    return True

def remove_permission(permission, group, obj):
    """Removes passed permission from passed group and object. Returns True if
    the permission has been removed.

    **Parameters:**

        permission
            The permission for which should be removed. Either a permission 
            object or the codename of a permission.
        group
            The group for which a permission should be removed.
        obj
            The content object for which a permission should be removed.
    """
    if not isinstance(permission, Permission):
        try:
            permission = Permission.objects.get(codename = permission)
        except Permission.DoesNotExist:
            return False

    ct = ContentType.objects.get_for_model(obj)
    try:
        op = ObjectPermission.objects.get(group=group, content_type = ct, content_id=obj.id, permission = permission)
    except ObjectPermission.DoesNotExist:
        return False

    op.delete()
    return True

def has_permission(codename, user, obj=None):
    """Checks whether the passed user has passed permission for passed object.

    **Parameters:**

    codename
        The permission's codename which should be checked.
    user
        The user for which the permission should be checked.
    obj
        The object for which the permission should be checked.
    """
    if user.is_superuser:
        return True

    if not user.is_authenticated():
        user = User.objects.get(username="anonymous")

    if obj is None:
        return False

    groups = Group.objects.filter(user=user)
    ct = ContentType.objects.get_for_model(obj)

    while obj is not None:
        p = ObjectPermission.objects.filter(
            content_type=ct, content_id=obj.id, group__in=groups, permission__codename = codename)

        if p.exists():
            return True

        if is_inherited(codename, obj):
            return False

        try:
            obj = obj.get_parent_for_permissions()
            ct = ContentType.objects.get_for_model(obj)
        except AttributeError:
            return False

    return False

# Inheritance ################################################################

def add_inheritance_block(permission, obj):
    """Adds an inheritance for the passed permission on the passed obj.

    **Parameters:**

        permission
            The permission for which an inheritance block should be added. 
            Either a permission object or the codename of a permission.
        obj
            The content object for which an inheritance block should be added.
    """
    if not isinstance(permission, Permission):
        try:
            permission = Permission.objects.get(codename = permission)
        except Permission.DoesNotExist:
            return False

    ct = ContentType.objects.get_for_model(obj)
    try:
        ObjectPermissionInheritanceBlock.objects.get(content_type = ct, content_id=obj.id, permission=permission)
    except ObjectPermissionInheritanceBlock.DoesNotExist:
        try:
            result = ObjectPermissionInheritanceBlock.objects.create(content=obj, permission=permission)
        except IntegrityError:
            return False
    return True

def remove_inheritance_block(permission, obj):
    """Removes a inheritance block for the passed permission from the passed 
    object.

    **Parameters:**

        permission
            The permission for which an inheritance block should be removed.
            Either a permission object or the codename of a permission.
        obj
            The content object for which an inheritance block should be added.
    """
    if not isinstance(permission, Permission):
        try:
            permission = Permission.objects.get(codename = permission)
        except Permission.DoesNotExist:
            return False

    ct = ContentType.objects.get_for_model(obj)
    try:
        opi = ObjectPermissionInheritanceBlock.objects.get(content_type = ct, content_id=obj.id, permission=permission)
    except ObjectPermissionInheritanceBlock.DoesNotExist:
        return False

    opi.delete()
    return True

def is_inherited(codename, obj):
    """Returns True if the passed permission is inherited for passed object.

    **Parameters:**

        codename
            The permission which should be checked. Must be the codename of
            the permission.
        obj
            The content object for which the permission should be checked.
    """
    ct = ContentType.objects.get_for_model(obj)
    try:
        ObjectPermissionInheritanceBlock.objects.get(
            content_type=ct, content_id=obj.id, permission__codename = codename)
    except ObjectDoesNotExist:
        return True
    else:
        return False

# Registering ################################################################

def register_permission(name, codename):
    """Registers a permission to the framework. Returns the permission if the
    registration was successfully, otherwise False.

    **Parameters:**

        name
            The unique name of the permission. This is displayed to the
            customer.

        codename
            The unique codename of the permission. This is used internally to
            identify the permission.
    """
    try:
        p = Permission.objects.create(name=name, codename=codename)
    except IntegrityError:
        return False
    return p

def unregister_permission(codename):
    """Unregisters a permission from the framework

    **Parameters:**

        codename
            The unique codename of the permission.
    """
    try:
        permission = Permission.objects.get(codename=codename)
    except Permission.DoesNotExist:
        return False
    permission.delete()
    return True

def register_group(name):
    """Registers a group with passed name to the framework. Creates a Django 
    default group. Returns the new group if the registration was successfully, 
    otherwise False.

    **Parameters:**

        name
            The unique group name.
    """
    try:
        group = Group.objects.create(name=name)
    except IntegrityError:
        return False
    return group

def unregister_group(name):
    """Unregisters the group with passed name. This will remove a Django
    default group with passed name.

    **Parameters:**

        name
            The unique group name.
    """
    try:
        group = Group.objects.get(name=name)
    except Group.DoesNotExist:
        return False

    group.delete()
    return True