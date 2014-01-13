# coding=utf-8
"""
Decorator utility module
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ['redirect_to_login']
import urlparse
from django.contrib.auth import REDIRECT_FIELD_NAME
from permission.conf import settings

def redirect_to_login(request, login_url=None,
                      redirect_field_name=REDIRECT_FIELD_NAME):
    """redirect to login"""
    path = request.build_absolute_uri()
    # if the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = \
            urlparse.urlparse(login_url or settings.LOGIN_URL)[:2]
    current_scheme, current_netloc = urlparse.urlparse(path)[:2]
    if ((not login_scheme or login_scheme == current_scheme) and
        (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()
    from django.contrib.auth.views import \
            redirect_to_login as auth_redirect_to_login
    return auth_redirect_to_login(path, login_url, redirect_field_name)
