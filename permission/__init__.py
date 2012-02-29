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
        raise ImproperlyConfigured(
                '"permission.backends.PermissionBackend" is not found in '
                '`AUTHENTICATION_BACKENDS`.'
            )

# Auto-discover INSTALLED_APPS permissions.py modules
if installed:
    autodiscover()
