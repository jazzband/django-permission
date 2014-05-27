# coding=utf-8
"""
Permission logic module for author based permission system
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from permission.conf import settings
from permission.logics.base import PermissionLogic
from permission.utils.field_lookup import field_lookup


class AuthorPermissionLogic(PermissionLogic):
    """
    Permission logic class for author based permission system
    """
    def __init__(self,
                 field_name=None,
                 any_permission=None,
                 change_permission=None,
                 delete_permission=None):
        """
        Constructor

        Parameters
        ----------
        field_name : string
            A field name of object which store the author as django user model.
            You can specify the related object with '__' like django queryset
            filter.
            Default value will be taken from
            ``PERMISSION_DEFAULT_APL_FIELD_NAME`` in
            settings.
        any_permission : boolean
            True for give any permission of the specified object to the author
            Default value will be taken from
            ``PERMISSION_DEFAULT_APL_ANY_PERMISSION`` in
            settings.
        change_permission : boolean
            True for give change permission of the specified object to the
            author.
            It will be ignored if :attr:`any_permission` is True.
            Default value will be taken from
            ``PERMISSION_DEFAULT_APL_CHANGE_PERMISSION`` in
            settings.
        delete_permission : boolean
            True for give delete permission of the specified object to the
            author.
            It will be ignored if :attr:`any_permission` is True.
            Default value will be taken from
            ``PERMISSION_DEFAULT_APL_DELETE_PERMISSION`` in
            settings.
        """
        self.field_name = field_name
        self.any_permission = any_permission
        self.change_permission = change_permission
        self.delete_permission = delete_permission

        if self.field_name is None:
            self.field_name = \
                settings.PERMISSION_DEFAULT_APL_FIELD_NAME
        if self.any_permission is None:
            self.any_permission = \
                settings.PERMISSION_DEFAULT_APL_ANY_PERMISSION
        if self.change_permission is None:
            self.change_permission = \
                settings.PERMISSION_DEFAULT_APL_CHANGE_PERMISSION
        if self.delete_permission is None:
            self.delete_permission = \
                settings.PERMISSION_DEFAULT_APL_DELETE_PERMISSION

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have permission (of object)

        If the user_obj is not authenticated, it return ``False``.

        If no object is specified, it return ``True`` when the corresponding
        permission was specified to ``True`` (changed from v0.7.0).
        This behavior is based on the django system.
        https://code.djangoproject.com/wiki/RowLevelPermissions

        If an object is specified, it will return ``True`` if the user is
        specified in ``field_name`` of the object (e.g. ``obj.author``).
        So once user create an object and the object store who is the author in
        ``field_name`` attribute (default: ``author``), the author can change
        or delete the object (you can change this behavior to set
        ``any_permission``, ``change_permissino`` or ``delete_permission``
        attributes of this instance).

        Parameters
        ----------
        user_obj : django user model instance
            A django user model instance which be checked
        perm : string
            `app_label.codename` formatted permission string
        obj : None or django model instance
            None or django model instance for object permission

        Returns
        -------
        boolean
            Wheter the specified user have specified permission (of specified
            object).
        """
        if not user_obj.is_authenticated():
            return False
        # construct the permission full name
        change_permission = self.get_full_permission_string('change')
        delete_permission = self.get_full_permission_string('delete')
        # check if the user is authenticated
        if obj is None:
            # object permission without obj should return True
            # Ref: https://code.djangoproject.com/wiki/RowLevelPermissions
            if self.any_permission:
                return True
            if self.change_permission and perm == change_permission:
                return True
            if self.delete_permission and perm == delete_permission:
                return True
            return False
        elif user_obj.is_active:
            # get author instance
            author = field_lookup(obj, self.field_name)
            if author == user_obj:
                if self.any_permission:
                    # have any kind of permissions to the obj
                    return True
                if (self.change_permission and
                        perm == change_permission):
                    return True
                if (self.delete_permission and
                        perm == delete_permission):
                    return True
        return False
