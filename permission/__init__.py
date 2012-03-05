import warnings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from utils import autodiscover
from handlers import registry
from handlers import PermissionHandler

__all__ = ('autodiscover', 'registry', 'PermissionHandler')

installed = 'permission' in settings.INSTALLED_APPS

# set default settings
def setconf(name, default_value):
    value = getattr(settings, name, default_value)
    setattr(settings, name, value)

setconf('PERMISSION_MODULE_NAME', 'permissions')
setconf('PERMISSION_BUILTIN_TEMPLATETAGS', True)
setconf('PERMISSION_REPLACE_BUILTIN_IF', True)
setconf('PERMISSION_EXTEND_USER_CLASS', True)

# validate settings
if installed:
    if 'django.contrib.auth' \
            not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured(
                '"django.contrib.auth" is not found in '
                '`INSTALLED_APPS`. You need to use "permission" '
                'with "django.contrib.auth".'
            )
    if 'permission.backends.PermissionBackend' \
            not in settings.AUTHENTICATION_BACKENDS:
        warnings.warn(Warning,
                '"permission.backends.PermissionBackend" is not found in '
                '`AUTHENTICATION_BACKENDS`.'
            )
    if 'permission.backends.RoleBackend' \
            not in settings.AUTHENTICATION_BACKENDS:
        warnings.warn(Warning,
                '"permission.backends.RoleBackend" is not found in '
                '`AUTHENTICATION_BACKENDS`.'
            )

# Register templatetags in builtin
if settings.PERMISSION_BUILTIN_TEMPLATETAGS:
    from django.template import add_to_builtins
    add_to_builtins('permission.templatetags.permission_tags')

# Extend User class
if settings.PERMISSION_EXTEND_USER_CLASS:
    from django.contrib import auth
    from django.contrib.auth.models import User
    from django.contrib.auth.models import AnonymousUser
    def _user_has_role(user, role):
        anon = user.is_anonymous()
        active = user.is_active
        for backend in auth.get_backends():
            if anon or active or backend.supports_inactive_user:
                if hasattr(backend, 'has_role'):
                    if backend.has_role(user, role):
                        return True
        return False
    def _user_get_all_roles(user):
        anon = user.is_anonymous()
        active = user.is_active
        for backend in auth.get_backends():
            if anon or active or backend.supports_inactive_user:
                if hasattr(backend, 'get_all_roles'):
                    return backend.get_all_roles(user)
        return None
    User.has_role = _user_has_role
    User.roles = property(_user_get_all_roles)
    AnonymousUser.has_role = lambda user, role: False
    AnonymousUser.roles = ()

# Auto-discover INSTALLED_APPS permissions.py modules
if installed:
    autodiscover()
