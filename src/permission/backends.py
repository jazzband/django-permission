# coding=utf-8
"""
Logical permission backends module
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ('PermissionBackend',)
from permission.utils.handlers import registry


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
        # get permission handlers fot this perm
        cache_name = '_%s_cache' % perm
        if hasattr(self, cache_name):
            handlers = getattr(self, cache_name)
        else:
            handlers = [h for h in registry.get_handlers()
                        if perm in h.get_permissions(user_obj, perm, obj=obj)]
            setattr(self, cache_name, handlers)
        for handler in handlers:
            if handler.has_perm(user_obj, perm, obj=obj):
                return True
        return False
