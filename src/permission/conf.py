# coding=utf-8
"""
django-permission application configure
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from appconf import AppConf
from permission.handlers import LogicalPermissionHandler


__all__ = ('settings',)


class PermissionConf(AppConf):
    DEFAULT_PERMISSION_HANDLER = 'permission.handlers.LogicalPermissionHandler'
    """Default permission handler class"""

    CHECK_PERMISSION_PRESENCE = settings.DEBUG
    """Check if the specified string permission exists"""

    REPLACE_BUILTIN_IF = True
    """Whether replace builtin if templatetag"""

    DEFAULT_APL_FIELD_NAME = 'author'
    DEFAULT_APL_ANY_PERMISSION = False
    DEFAULT_APL_CHANGE_PERMISSION = True
    DEFAULT_APL_DELETE_PERMISSION = True

    DEFAULT_CPL_FIELD_NAME = 'collaborators'
    DEFAULT_CPL_ANY_PERMISSION = False
    DEFAULT_CPL_CHANGE_PERMISSION = True
    DEFAULT_CPL_DELETE_PERMISSION = False

    DEFAULT_GIPL_ANY_PERMISSION = False
    DEFAULT_GIPL_ADD_PERMISSION = True
    DEFAULT_GIPL_CHANGE_PERMISSION = True
    DEFAULT_GIPL_DELETE_PERMISSION = False

    DEFAULT_OSPL_ANY_PERMISSION = False
    DEFAULT_OSPL_CHANGE_PERMISSION = True
    DEFAULT_OSPL_DELETE_PERMISSION = True

    DEFAULT_SPL_ANY_PERMISSION = False
    DEFAULT_SPL_ADD_PERMISSION = True
    DEFAULT_SPL_CHANGE_PERMISSION = True
    DEFAULT_SPL_DELETE_PERMISSION = False

    AUTODISCOVER_MODULE_NAME = 'perms'
    AUTODISCOVER_VARIABLE_NAME = 'PERMISSION_LOGICS'
    AUTODISCOVER_ENABLE = True

    CHECK_AUTHENTICATION_BACKENDS = True
    """Check if AUTHENTICATION_BACKENDS is correctly configured"""

    CHECK_TEMPLATES_OPTIONS_BUILTINS = True
    """Check if TEMPLATES[?]['OPTIONS']['builtins'] is correctly configured"""
