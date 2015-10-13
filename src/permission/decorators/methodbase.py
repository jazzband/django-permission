# coding=utf-8
"""
permission_required decorator for generic classbased/functionbased view
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import wraps
from django.http import HttpRequest
from django.utils.decorators import available_attrs
from django.core.exceptions import PermissionDenied

from permission.decorators.utils import redirect_to_login


def permission_required(perm, queryset=None,
                        login_url=None, raise_exception=False):
    """
    Permission check decorator for classbased/functionbased generic view

    This decorator works as method or function decorator
    DO NOT use ``method_decorator`` or whatever while this decorator will use
    ``self`` argument for method of classbased generic view.

    Parameters
    ----------
    perm : string
        A permission string
    queryset_or_model : queryset or model
        A queryset or model for finding object.
        With classbased generic view, ``None`` for using view default queryset.
        When the view does not define ``get_queryset``, ``queryset``,
        ``get_object``, or ``object`` then ``obj=None`` is used to check
        permission.
        With functional generic view, ``None`` for using passed queryset.
        When non queryset was passed then ``obj=None`` is used to check
        permission.

    Examples
    --------
    >>> # As method decorator
    >>> class UpdateAuthUserView(UpdateView):
    >>>     @permission_required('auth.change_user')
    >>>     def dispatch(self, request, *args, **kwargs):
    ...         pass
    >>> # As function decorator
    >>> @permission_required('auth.change_user')
    >>> def update_auth_user(request, *args, **kwargs):
    ...     pass
    """
    def wrapper(view_method):
        @wraps(view_method, assigned=available_attrs(view_method))
        def inner(self, request=None, *args, **kwargs):
            if isinstance(self, HttpRequest):
                from permission.decorators.functionbase import \
                        permission_required as decorator
                # this is a functional view not classbased view.
                decorator = decorator(perm, queryset,
                                      login_url, raise_exception)
                decorator = decorator(view_method)
                if not request:
                    args = list(args)
                    args.insert(0, request)
                request = self
                return decorator(request, *args, **kwargs)
            else:
                from permission.decorators.classbase import \
                        get_object_from_classbased_instance
                # get object
                obj = get_object_from_classbased_instance(
                        self, queryset, request, *args, **kwargs
                    )
                
                if not request.user.has_perm(perm, obj=obj):
                    if raise_exception:
                        raise PermissionDenied
                    else:
                        return redirect_to_login(request, login_url)
                return view_method(self, request, *args, **kwargs)
        return inner
    return wrapper
