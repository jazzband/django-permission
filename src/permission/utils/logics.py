# coding=utf-8
"""
Permission logic utilities
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from permission.logics import PermissionLogic


def add_permission_logic(model, permission_logic):
    """
    Add permission logic to the model

    Parameters
    ----------
    model : django model class
        A django model class which will be treated by the specified permission
        logic
    permission_logic : permission logic class
        A permission logic class with will be used to determine permission of
        the model

    Examples
    --------
    >>> from django.db import models
    >>> from permission.logics import PermissionLogic
    >>> class Mock(models.Model):
    ...     name = models.CharField('name', max_length=120)
    >>> add_permission_logic(Mock, PermissionLogic())
    """
    if not isinstance(permission_logic, PermissionLogic):
        raise AttributeError(
        '`permission_logic` must be an instance of PermissionLogic')
    if not hasattr(model, '_permission_logics'):
        model._permission_logics = set()
    if not hasattr(model, '_permission_handler'):
        from permission.utils.handlers import registry
        # register default permission handler
        registry.register(model, handler=None)
    model._permission_logics.add(permission_logic)

def remove_permission_logic(model, permission_logic, fail_silently=True):
    """
    Remove permission logic to the model

    Parameters
    ----------
    model : django model class
        A django model class which will be treated by the specified permission
        logic
    permission_logic : permission logic class
        A permission logic class with will be used to determine permission of
        the model
    fail_silently : boolean
        If `True` then do not raise KeyError even the specified permission logic
        have not registered.
    
    Examples
    --------
    >>> from django.db import models
    >>> from permission.logics import PermissionLogic
    >>> class Mock(models.Model):
    ...     name = models.CharField('name', max_length=120)
    >>> logic = PermissionLogic()
    >>> add_permission_logic(Mock, logic)
    >>> remove_permission_logic(Mock, logic)
    """
    if not isinstance(permission_logic, PermissionLogic):
        raise AttributeError(
        '`permission_logic` must be an instance of PermissionLogic')
    if not hasattr(model, '_permission_logics'):
        model._permission_logics = set()
    if fail_silently and permission_logic not in model._permission_logics:
        pass
    else:
        model._permission_logics.remove(permission_logic)

