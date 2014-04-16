# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from permission.conf import settings
from permission.utils.permissions import get_app_perms
from permission.utils.permissions import get_model_perms
from permission.utils.permissions import perm_to_permission
import collections


class PermissionHandler(object):
    """
    Abstract permission handler class
    """
    _includes = None
    _excludes = None

    @property
    def includes(self):
        return self._includes
    @includes.setter
    def includes(self, value):
        # clear cache
        if hasattr(self, '_perms_cache'):
            del self._perms_cache
        self._includes = value

    @property
    def excludes(self):
        return self._excludes
    @excludes.setter
    def excludes(self, value):
        # clear cache
        if hasattr(self, '_perms_cache'):
            del self._perms_cache
        self._excludes = value


    def __init__(self, model_or_app_label):
        """
        Constructor

        Parameters
        ----------
        model_or_app_label : django model class or string
            A django model class or application label string.
            Use django model class for model level permission and application
            label for application level permission.
        """
        if isinstance(model_or_app_label, str):
            self.app_label = model_or_app_label
            self.model = None
            if self.includes is None:
                self.includes = self._get_app_perms
        else:
            self.app_label = model_or_app_label._meta.app_label
            self.model = model_or_app_label
            self.model._permission_handler = self
            if self.includes is None:
                self.includes = self._get_model_perms

    def _get_app_perms(self, *args):
        """
        Get permissions related to the application specified in constructor

        Returns
        -------
        set
            A set instance of `app_label.codename` formatted permission strings
        """
        if not hasattr(self, '_app_perms_cache'):
            self._app_perms_cache = get_app_perms(self.app_label)
        return self._app_perms_cache

    def _get_model_perms(self, *args):
        """
        Get permissions related to the model specified in constructor

        Returns
        -------
        set
            A set instance of `app_label.codename` formatted permission strings
        """
        if not hasattr(self, '_model_perms_cache'):
            if self.model is None:
                self._model_perms_cache = set()
            else:
                self._model_perms_cache = get_model_perms(self.model)
        return self._model_perms_cache

    def get_permissions(self, user_obj, perm, obj=None):
        """
        Get permissions which this handler can treat.
        Specified with :attr:`includes` and :attr:`excludes` of this instance.

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
        set
            A set instance of `app_label.codename` formatted permission strings
        """
        if not hasattr(self, '_perms_cache'):
            if self.includes and isinstance(self.includes, collections.Callable):
                includes = self.includes(self)
            else:
                includes = self.includes or []
            if self.excludes and isinstance(self.excludes, collections.Callable):
                excludes = self.excludes(self)
            else:
                excludes = self.excludes or []
            includes = set(includes)
            excludes = set(excludes)
            includes = includes.difference(excludes)
            self._perms_cache = includes
        return self._perms_cache

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
                "method. Sub class must override this method." % self.__class__)

class LogicalPermissionHandler(PermissionHandler):
    """
    Permission handler class which use permission logics to determine the
    permission
    """

    def __init__(self, model):
        """
        Constructor

        Parameters
        ----------
        model : django model class
            A django model class.

        .. note::
            LogicalPermissionHandler cannot treat application level permission
        """
        # logical permission handler cannot treat application level permission
        if isinstance(model, str):
            raise AttributeError(
                    "'%s' cannot treat application level permission." %
                    self.__class__)
        super(LogicalPermissionHandler, self).__init__(model)

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have permission (of object) based on
        specified models's ``_permission_logics`` attribute.

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

        if perm not in self.get_permissions(user_obj, perm, obj=obj):
            return False
        for permission_logic in getattr(self.model, '_permission_logics', []):
            if permission_logic.has_perm(user_obj, perm, obj):
                return True
        return False
