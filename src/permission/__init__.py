# coding=utf-8
"""
django-permission
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from app_version import get_versions
__version__, VERSION = get_versions('django-permission', allow_ambiguous=True)
# load shortcut functions
from permission.utils.logics import add_permission_logic
from permission.utils.logics import remove_permission_logic

# autodiscover
from permission.conf import settings
from permission.utils.autodiscover import autodiscover
if settings.PERMISSION_AUTODISCOVER_ENABLE:
    autodiscover()
