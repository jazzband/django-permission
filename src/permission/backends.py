# coding=utf-8
"""
Logical permission backends module
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ('PermissionBackend',)
from permission.conf import settings
from permission.utils.handlers import registry
from permission.utils.permissions import perm_to_permission


class PermissionBackend(object):
    """
    A handler based permission backend
    """
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        """
        Always return ``None`` to prevent authentication within this backend.
        """
        return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have permission (of object) based on registered handlers.

        It will raise ``ObjectDoesNotExist`` exception when the specified
        string permission does not exist and
        ``PERMISSION_CHECK_PERMISSION_PRESENCE`` is ``True`` in ``settings``
        module.

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

        Raises
        ------
        django.core.exceptions.ObjectDoesNotExist
            If the specified string permission does not exist and
            ``PERMISSION_CHECK_PERMISSION_PRESENCE`` is ``True`` in ``settings``
            module.
        """
        if settings.PERMISSION_CHECK_PERMISSION_PRESENCE:
            # get permission instance from string permission (perm)
            # it raise ObjectDoesNotExists when the permission is not exists
            perm_to_permission(perm)

        # get permission handlers fot this perm
        cache_name = '_%s_cache' % perm
        if hasattr(self, cache_name):
            handlers = getattr(self, cache_name)
        else:
            handlers = [h for h in registry.get_handlers()
                        if perm in h.get_supported_permissions()]
            setattr(self, cache_name, handlers)
        for handler in handlers:
            if handler.has_perm(user_obj, perm, obj=obj):
                return True
        return False

    def has_module_perms(self, user_obj, app_label):
        """
        Check if user have permission of specified app based on registered
        handlers.

        It will raise ``ObjectDoesNotExist`` exception when the specified
        string permission does not exist and
        ``PERMISSION_CHECK_PERMISSION_PRESENCE`` is ``True`` in ``settings``
        module.

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

        Raises
        ------
        django.core.exceptions.ObjectDoesNotExist
            If the specified string permission does not exist and
            ``PERMISSION_CHECK_PERMISSION_PRESENCE`` is ``True`` in ``settings``
            module.
        """
        # get permission handlers fot this perm
        cache_name = '_%s_cache' % app_label
        if hasattr(self, cache_name):
            handlers = getattr(self, cache_name)
        else:
            handlers = [h for h in registry.get_handlers()
                        if app_label in h.get_supported_app_labels()]
            setattr(self, cache_name, handlers)
        for handler in handlers:
            if handler.has_module_perms(user_obj, app_label):
                return True
        return False
