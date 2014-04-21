# coding=utf-8
"""
django-permission application configure
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ('settings',)
from django.conf import settings
from appconf import AppConf
from permission.handlers import LogicalPermissionHandler

class PermissionConf(AppConf):
    DEFAULT_PERMISSION_HANDLER = LogicalPermissionHandler
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

    AUTODISCOVER_ENABLE = True
    AUTODISCOVER_MODULE_NAME = 'perms'
    AUTODISCOVER_VARIABLE_NAME = 'PERMISSION_LOGICS'
