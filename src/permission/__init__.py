from app_version import get_versions
__version__, VERSION = get_versions('django-permission', allow_ambiguous=True)

# load shortcut functions
from permission.utils.logics import add_permission_logic
from permission.utils.logics import remove_permission_logic

# autodiscover
from permission.utils.autodiscover import autodiscover

from permission.conf import settings
from django.core.exceptions import ImproperlyConfigured

if 'permission' in settings.INSTALLED_APPS:
    if settings.PERMISSION_CHECK_AUTHENTICATION_BACKENDS:
        if ('permission.backends.PermissionBackend' not in
                settings.AUTHENTICATION_BACKENDS):
            raise ImproperlyConfigured(
                    '"permission.backends.PermissionBackend" is not found in '
                    '`AUTHENTICATION_BACKENDS`.\n'
                    'Users require to specify the backend manually to the '
                    'option.\n'
                    'Users can ignore this exception via setting `False` to '
                    '`PERMISSION_CHECK_AUTHENTICATION_BACKENDS`.'
                )
    if settings.PERMISSION_REPLACE_BUILTIN_IF:
        from permission.compat import add_to_builtins
        if add_to_builtins:
            add_to_builtins('permission.templatetags.permissionif')
        elif settings.PERMISSION_CHECK_TEMPLATES_OPTIONS_BUILTINS:
            from django.core.exceptions import ImproperlyConfigured
            # Check if settings.TEMPLATES[?]['OPTIONS']['builtins'] has
            # 'permission.templatetags.permissionif'
            def has_permissionif_in_builtins():
                for template in settings.TEMPLATES:
                    OPTIONS  = template.get('OPTIONS', {})
                    builtins = OPTIONS.get('builtins', [])
                    for builtin in builtins:
                        if builtin == 'permission.templatetags.permissionif':
                            return True
                return False
            if not has_permissionif_in_builtins():
                raise ImproperlyConfigured(
                    '"permission.templatetags.permissionif" is not found in '
                    'none of `TEMPLATES[?][\'OPTIONS\'][\'builtins\']`.\n'
                    'From Django 1.9, users require to specify the module '
                    'to the option for loading a templatetag automatically '
                    'or load the module manually.\n'
                    'Users can ignore this exception via setting `False` to '
                    '`PERMISSION_CHECK_TEMPLATES_OPTIONS_BUILTINS`.'
                )
