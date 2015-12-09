from app_version import get_versions
__version__, VERSION = get_versions('django-permission', allow_ambiguous=True)

# load shortcut functions
from permission.utils.logics import add_permission_logic
from permission.utils.logics import remove_permission_logic

# autodiscover
from permission.utils.autodiscover import autodiscover

# builtin
from permission.conf import settings
if settings.PERMISSION_REPLACE_BUILTIN_IF:
    from permission.compat import add_to_builtins
    if add_to_builtins:
        # add_to_builtins was removed from Django 1.9
        add_to_builtins('permission.templatetags.permissionif')
