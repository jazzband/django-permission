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
    permission_logic : permission logic instance
        A permission logic instance which will be used to determine permission
        of the model

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
    # store target model to the permission_logic instance
    permission_logic.model = model

def remove_permission_logic(model, permission_logic, fail_silently=True):
    """
    Remove permission logic to the model

    Parameters
    ----------
    model : django model class
        A django model class which will be treated by the specified permission
        logic
    permission_logic : permission logic class or instance
        A permission logic class or instance which will be used to determine
        permission of the model
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
    if not hasattr(model, '_permission_logics'):
        model._permission_logics = set()
    if not isinstance(permission_logic, PermissionLogic):
        # remove all permission logic of related
        remove_set = set()
        for _permission_logic in model._permission_logics:
            if _permission_logic.__class__ == permission_logic:
                remove_set.add(_permission_logic)
        # difference
        model._permission_logics = model._permission_logics.difference(remove_set)
    else:
        if fail_silently and permission_logic not in model._permission_logics:
            pass
        else:
            model._permission_logics.remove(permission_logic)

