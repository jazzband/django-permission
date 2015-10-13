# coding=utf-8
"""
permission_required decorator for generic classbased view from django 1.3
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import wraps
from django.utils.decorators import available_attrs
from django.core.exceptions import PermissionDenied

from permission.decorators.utils import redirect_to_login

def permission_required(perm, queryset=None,
                        login_url=None, raise_exception=False):
    """
    Permission check decorator for classbased generic view

    This decorator works as class decorator
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
    >>> @permission_required('auth.change_user')
    >>> class UpdateAuthUserView(UpdateView):
    ...     pass
    """
    def wrapper(cls):
        def view_wrapper(view_func):
            @wraps(view_func, assigned=available_attrs(view_func))
            def inner(self, request, *args, **kwargs):
                # get object
                obj = get_object_from_classbased_instance(
                        self, queryset, request, *args, **kwargs
                    )

                if not request.user.has_perm(perm, obj=obj):
                    if raise_exception:
                        raise PermissionDenied
                    else:
                        return redirect_to_login(request, login_url)
                return view_func(self, request, *args, **kwargs)
            return inner
        cls.dispatch = view_wrapper(cls.dispatch)
        return cls
    return wrapper


def get_object_from_classbased_instance(
        instance, queryset, request, *args, **kwargs):
    """
    Get object from an instance of classbased generic view
    
    Parameters
    ----------
    instance : instance
        An instance of classbased generic view
    queryset : instance
        A queryset instance
    request : instance
        A instance of HttpRequest

    Returns
    -------
    instance
        An instance of model object or None
    """
    from django.views.generic.edit import BaseCreateView
    # initialize request, args, kwargs of classbased_instance
    # most of methods of classbased view assumed these attributes
    # but these attributes is initialized in ``dispatch`` method.
    instance.request = request
    instance.args = args
    instance.kwargs = kwargs

    # get queryset from class if ``queryset_or_model`` is not specified
    if hasattr(instance, 'get_queryset') and not queryset:
        queryset = instance.get_queryset()
    elif hasattr(instance, 'queryset') and not queryset:
        queryset = instance.queryset
    elif hasattr(instance, 'model') and not queryset:
        queryset = instance.model._default_manager.all()
        
    # get object
    if hasattr(instance, 'get_object'):
        try:
            obj = instance.get_object(queryset)
        except AttributeError as e:
            # CreateView has ``get_object`` method but CreateView
            # should not have any object before thus simply set
            # None
            if isinstance(instance, BaseCreateView):
                obj = None
            else:
                raise e
    elif hasattr(instance, 'object'):
        obj = instance.object
    else:
        obj = None
    return obj

