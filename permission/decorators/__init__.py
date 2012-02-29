import inspect
from django.db.models.base import ModelBase

from class_decorators import permission_required as class_permission_required
from method_decorators import permission_required as method_permission_required

__all__ = ['permission_required']


def permission_required(perm, queryset_or_model=None, login_url=None, raise_exception=False):
    """Permission check decorator for classbased/functional generic view

    This decorator works as class, method or function decorator without modification.
    DO NOT use ``method_decorator`` or whatever whilte this decorator will use
    ``self`` argument for method of classbased generic view.

    Arguments:

        perm
            permission string

        queryset_or_model
            a queryset or model for finding object. With classbased generic
            view, ``None`` for using view default queryset. When the view does
            not define ``get_queryset``, ``queryset``, ``get_object`` and ``object``
            then ``obj=None`` is used to check permission. With functional generic
            view, ``None`` for using passed queryset. When non queryset was passed
            then ``obj=None`` is used to check permission.

    Usage:

        # As class decorator
        @permission_required('auth.change_user')
        class UpdateAuthUserView(UpdateView):
            # ...

        # As method decorator
        class UpdateAuthUserView(UpdateView):
            @permission_required('auth.change_user')
            def dispatch(self, request, *args, **kwargs):
                # ...
        
        # As function decorator
        @permission_required('auth.change_user')
        def update_auth_user(request, *args, **kwargs):
            # ...

    .. Note::
        Classbased generic view is recommended while you can regulate the queryset
        with ``get_queryset()`` method. Detecting object from passed kwargs may
        not work correctly.

    """
    # convert model to queryset
    if issubclass(queryset_or_model, ModelBase):
        queryset_or_model = queryset_or_model._default_manager.all()

    def wrapper(class_or_method):
        if inspect.isclass(class_or_method):
            decorator = class_permission_required
        else:
            # method_permission_required can handle method or function
            # correctly.
            decorator = method_permission_required
        return decorator(perm, queryset_or_model, login_url, raise_exception)(class_or_method)
    return wrapper
