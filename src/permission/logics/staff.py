# coding=utf-8
"""
Permission logic module for author based permission system
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from permission.conf import settings
from permission.logics.base import PermissionLogic


class StaffPermissionLogic(PermissionLogic):
    """
    Permission logic class for is_staff authority based permission system
    """
    def __init__(self,
                 any_permission=None,
                 add_permission=None,
                 change_permission=None,
                 delete_permission=None):
        """
        Constructor

        Parameters
        ----------
        any_permission : boolean
            True for give any permission of the specified object to the staff
            user. Default value will be taken from
            ``PERMISSION_DEFAULT_SPL_ANY_PERMISSION`` in
            settings.
        add_permission : boolean
            True for give change permission of the specified object to the
            staff user.
            It will be ignored if :attr:`any_permission` is True.
            Default value will be taken from
            ``PERMISSION_DEFAULT_SPL_ADD_PERMISSION`` in
            settings.
        change_permission : boolean
            True for give change permission of the specified object to the
            staff user.
            It will be ignored if :attr:`any_permission` is True.
            Default value will be taken from
            ``PERMISSION_DEFAULT_SPL_CHANGE_PERMISSION`` in
            settings.
        delete_permission : boolean
            True for give delete permission of the specified object to the
            staff user.
            It will be ignored if :attr:`any_permission` is True.
            Default value will be taken from
            ``PERMISSION_DEFAULT_SPL_DELETE_PERMISSION`` in
            settings.
        """
        self.any_permission = any_permission
        self.add_permission = add_permission
        self.change_permission = change_permission
        self.delete_permission = delete_permission

        if self.any_permission is None:
            self.any_permission = \
                settings.PERMISSION_DEFAULT_SPL_ANY_PERMISSION
        if self.add_permission is None:
            self.add_permission = \
                settings.PERMISSION_DEFAULT_SPL_ADD_PERMISSION
        if self.change_permission is None:
            self.change_permission = \
                settings.PERMISSION_DEFAULT_SPL_CHANGE_PERMISSION
        if self.delete_permission is None:
            self.delete_permission = \
                settings.PERMISSION_DEFAULT_SPL_DELETE_PERMISSION

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have permission (of object)

        If the user_obj is not authenticated, it return ``False``.

        If no object is specified, it return ``True`` when the corresponding
        permission was specified to ``True`` (changed from v0.7.0).
        This behavior is based on the django system.
        https://code.djangoproject.com/wiki/RowLevelPermissions

        If an object is specified, it will return ``True`` if the user is
        staff. The staff can add, change or delete the object (you can change
        this behavior to set ``any_permission``, ``add_permission``,
        ``change_permission``, or ``delete_permission`` attributes of this
        instance).

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
            Weather the specified user have specified permission (of specified
            object).
        """
        if not user_obj.is_authenticated():
            return False
        # construct the permission full name
        add_permission = self.get_full_permission_string('add')
        change_permission = self.get_full_permission_string('change')
        delete_permission = self.get_full_permission_string('delete')
        if obj is None:
            if user_obj.is_staff:
                if self.add_permission and perm == add_permission:
                    return True
                if self.change_permission and perm == change_permission:
                    return True
                if self.delete_permission and perm == delete_permission:
                    return True
                return self.any_permission
            return False
        elif user_obj.is_active:
            if user_obj.is_staff:
                if self.any_permission:
                    # have any kind of permissions to the obj
                    return True
                if (self.add_permission and
                        perm == add_permission):
                    return True
                if (self.change_permission and
                        perm == change_permission):
                    return True
                if (self.delete_permission and
                        perm == delete_permission):
                    return True
        return False
