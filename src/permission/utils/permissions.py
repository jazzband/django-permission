# coding=utf-8
"""
Permission utility module.

In this module, term *perm* indicate the identifier string permission written
in 'app_label.codename' format.
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.contrib.auth.models import Permission


def get_perm_codename(perm, fail_silently=True):
    """
    Get permission codename from permission string

    Examples
    --------
    >>> get_perm_codename('app_label.codename_model') == 'codename_model'
    True
    >>> get_perm_codename('app_label.codename') == 'codename'
    True
    >>> get_perm_codename('codename_model') == 'codename_model'
    True
    >>> get_perm_codename('codename') == 'codename'
    True
    >>> get_perm_codename('app_label.app_label.codename_model') == 'app_label.codename_model'
    True
    """
    try:
        perm = perm.split('.', 1)[1]
    except IndexError as e:
        if not fail_silently:
            raise e
    return perm

def permission_to_perm(permission):
    """
    Convert a django permission instance to a identifier string permission
    format in 'app_label.codename' (termed as *perm*).

    Examples
    --------
    >>> permission = Permission.objects.get(
    ...     content_type__app_label='auth',
    ...     codename='add_user',
    ... )
    >>> permission_to_perm(permission) == 'auth.add_user'
    True
    """
    app_label = permission.content_type.app_label
    codename = permission.codename
    return "%s.%s" % (app_label, codename)

def perm_to_permission(perm):
    """
    Convert a identifier string permission format in 'app_label.codename'
    (teremd as *perm*) to a django permission instance.

    Examples
    --------
    >>> permission = perm_to_permission('auth.add_user')
    >>> permission.content_type.app_label == 'auth'
    True
    >>> permission.codename == 'add_user'
    True
    """
    try:
        app_label, codename = perm.split('.', 1)
    except IndexError:
        raise AttributeError(
                "The format of identifier string permission (perm) is wrong. "
                "It should be in 'app_label.codename'."
            )
    else:
        permission = Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename
            )
        return permission

def get_app_perms(model_or_app_label):
    """
    Get *perm* (a string in format of 'app_label.codename') list of the
    specified django application.

    Parameters
    ----------
    model_or_app_label : model class or string
        A model class or app_label string to specify the particular django
        application.

    Returns
    -------
    set
        A set of perms of the specified django application.

    Examples
    --------
    >>> perms1 = get_app_perms('auth')
    >>> perms2 = get_app_perms(Permission)
    >>> perms1 == perms2
    True
    """
    if not isinstance(model_or_app_label, str):
        # assume model_or_app_label is model class
        app_label = model_or_app_label._meta.app_label
    else:
        app_label = model_or_app_label
    qs = Permission.objects.filter(content_type__app_label=app_label)
    perms = ["%s.%s" % (app_label, p.codename) for p in qs.iterator()]
    return set(perms)

def get_model_perms(model):
    """
    Get *perm* (a string in format of 'app_label.codename') list of the
    specified django model.

    Parameters
    ----------
    model : model class
        A model class to specify the particular django model.

    Returns
    -------
    set
        A set of perms of the specified django model.

    Examples
    --------
    >>> sorted(get_model_perms(Permission)) == ['auth.add_permission', 'auth.change_permission', 'auth.delete_permission']
    True
    """
    app_label = model._meta.app_label
    model_name = model._meta.object_name.lower()
    qs = Permission.objects.filter(content_type__app_label=app_label,
                                   content_type__model=model_name)
    perms = ["%s.%s" % (app_label, p.codename) for p in qs.iterator()]
    return set(perms)

