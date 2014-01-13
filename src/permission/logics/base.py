# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'


class PermissionLogic(object):
    """
    Abstract permission logic class
    """
    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have permission (of object)

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

        .. note::
            Sub class must override this method.
        """
        raise NotImplementedError(
                "'%s' does not override `has_perm(user_obj, perm, obj=None)` "
                "method. Sub class of `PermissionLogic` must override this "
                "method.")
