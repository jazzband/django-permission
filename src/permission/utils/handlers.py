# coding=utf-8
"""
A utilities of permission handler
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import inspect
from permission.conf import settings
from django.core.exceptions import ImproperlyConfigured


class PermissionHandlerRegistry(object):
    """
    A registry class of permission handler
    """
    def __init__(self):
        self._registry = {}

    def register(self, model, handler=None):
        """
        Register a permission handler to the model

        Parameters
        ----------
        model : django model class
            A django model class
        handler : permission handler class or None
            A permission handler class

        Raises
        ------
        ImproperlyConfigured
            Raise when the model is abstract model
        KeyError
            Raise when the model is already registered in registry
            The model cannot have more than one handler.
        """
        from permission.handlers import PermissionHandler
        if model._meta.abstract:
            raise ImproperlyConfigured(
                    'The model %s is abstract, so it cannot be registered '
                    'with permission.' % model)
        if model in self._registry:
            raise KeyError("A permission handler class is already "
                            "registered for '%s'" % model)
        if handler is None:
            handler = settings.PERMISSION_DEFAULT_PERMISSION_HANDLER
        if not inspect.isclass(handler):
            raise AttributeError(
                    "`handler` attribute must be a class. "
                    "An instance was specified.")
        if not issubclass(handler, PermissionHandler):
            raise AttributeError(
                    "`handler` attribute must be a subclass of "
                    "`permission.handlers.PermissionHandler`")

        # Instantiate the handler to save in the registry
        instance = handler(model)
        self._registry[model] = instance

    def unregister(self, model):
        """
        Unregister a permission handler from the model

        Parameters
        ----------
        model : django model class
            A django model class
        handler : permission handler class or None
            A permission handler class

        Raises
        ------
        KeyError
            Raise when the model have not registered in registry yet.
        """
        if model not in self._registry:
            raise KeyError("A permission handler class have not been "
                            "registered for '%s' yet" % model)
        # remove from registry
        del self._registry[model]

    def get_handlers(self):
        """
        Get registered handler instances

        Returns
        -------
        tuple
            permission handler tuple
        """
        return tuple(self._registry.values())

"""Permission handler registry instance"""
registry = PermissionHandlerRegistry()
