# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
# coding=utf-8
"""
Decorator module for permission
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ['permission_required']
import inspect
from django.db.models import Model


def permission_required(perm, queryset_or_model=None,
                        login_url=None, raise_exception=False):
    """
    Permission check decorator for classbased/functional generic view

    This decorator works as class, method or function decorator without any
    modification.
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
    >>> # As class decorator
    >>> @permission_required('auth.change_user')
    >>> class UpdateAuthUserView(UpdateView):
    ...     pass
    >>> # As method decorator
    >>> class UpdateAuthUserView(UpdateView):
    ...     @permission_required('auth.change_user')
    ...     def dispatch(self, request, *args, **kwargs):
    ...         pass
    >>> # As function decorator
    >>> @permission_required('auth.change_user')
    >>> def update_auth_user(request, *args, **kwargs):
    ...     pass

    .. Note::
        Classbased generic view is recommended while you can regulate the queryset
        with ``get_queryset()`` method.
        Detecting object from passed kwargs may not work correctly.
    """
    # convert model to queryset
    if queryset_or_model and issubclass(queryset_or_model, Model):
        queryset_or_model = queryset_or_model._default_manager.all()

    def wrapper(class_or_method):
        if inspect.isclass(class_or_method):
            from permission.decorators.classbase import \
                    permission_required as decorator
        else:
            # method_permission_required can handle method or function
            # correctly.
            from permission.decorators.methodbase import \
                    permission_required as decorator
        return decorator(perm, queryset_or_model,
                         login_url, raise_exception)(class_or_method)
    return wrapper
