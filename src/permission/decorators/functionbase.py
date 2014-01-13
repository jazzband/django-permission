# coding=utf-8
"""
permission_required decorator for generic function view
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import copy
from functools import wraps
from django.shortcuts import get_object_or_404
from django.utils.decorators import available_attrs
from django.core.exceptions import PermissionDenied

from permission.decorators.utils import redirect_to_login


def permission_required(perm, queryset=None,
                        login_url=None, raise_exception=False):
    """
    Permission check decorator for function-base generic view

    This decorator works as function decorator

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
    >>> def update_auth_user(request, *args, **kwargs):
    ...     pass
    """
    def wrapper(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def inner(request, *args, **kwargs):
            _kwargs = copy.copy(kwargs)
            # overwrite queryset if specified
            if queryset:
                _kwargs['queryset'] = queryset

            # get object from view
            if 'date_field' in _kwargs:
                fn = get_object_from_date_based_view
            else:
                fn = get_object_from_list_detail_view
            if fn.validate(request, *args, **_kwargs):
                obj = fn(request, *args, **_kwargs)
            else:
                # required arguments is not passed
                obj = None

            if not request.user.has_perm(perm, obj=obj):
                if raise_exception:
                    raise PermissionDenied
                else:
                    return redirect_to_login(request, login_url)
            return view_func(request, *args, **_kwargs)
        return inner
    return wrapper


def get_object_from_list_detail_view(request, *args, **kwargs):
    """
    Get object from generic list_detail.detail view

    Parameters
    ----------
    request : instance
        An instance of HttpRequest

    Returns
    -------
    instance
        An instance of model object or None
    """
    queryset = kwargs['queryset']
    object_id = kwargs.get('object_id', None)
    slug = kwargs.get('slug', None)
    slug_field = kwargs.get('slug_field', 'slug')
    if object_id:
        obj = get_object_or_404(queryset, pk=object_id)
    elif slug and slug_field:
        obj = get_object_or_404(queryset, **{slug_field: slug})
    else:
        raise AttributeError(
                "Generic detail view must be called with either an "
                "object_id or a slug/slug_field."
            )
    return obj
def _get_object_from_list_detail_view_validation(request, *args, **kwargs):
    if 'queryset' not in kwargs:
        return False
    elif 'object_id' not in kwargs and 'slug' not in kwargs:
        return False
    return True
get_object_from_list_detail_view.validate = \
        _get_object_from_list_detail_view_validation


def get_object_from_date_based_view(request, *args, **kwargs):
    """
    Get object from generic date_based.detail view

    Parameters
    ----------
    request : instance
        An instance of HttpRequest

    Returns
    -------
    instance
        An instance of model object or None
    """
    import time
    import datetime
    from django.http import Http404
    from django.db.models.fields import DateTimeField
    try:
        from django.utils import timezone
        datetime_now = timezone.now
    except ImportError:
        datetime_now = datetime.datetime.now
    year, month, day = kwargs['year'], kwargs['month'], kwargs['day']
    month_format = kwargs.get('month_format', '%b')
    day_format = kwargs.get('day_format', '%d')
    date_field = kwargs['date_field']
    queryset = kwargs['queryset']
    object_id = kwargs.get('object_id', None)
    slug = kwargs.get('slug', None)
    slug_field = kwargs.get('slug_field', 'slug')
    
    try:
        tt = time.strptime(
                '%s-%s-%s' % (year, month, day),
                '%s-%s-%s' % ('%Y', month_format, day_format)
            )
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    model = queryset.model

    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {
                '%s__range' % date_field: (
                    datetime.datetime.combine(date, datetime.time.min),
                    datetime.datetime.combine(date, datetime.time.max),
                )}
    else:
        lookup_kwargs = {date_field: date}

    now = datetime_now()
    if date >= now.date() and not kwargs.get('allow_future', False):
        lookup_kwargs['%s__lte' % date_field] = now
    if object_id:
        lookup_kwargs['pk'] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        raise AttributeError(
                "Generic detail view must be called with either an "
                "object_id or a slug/slug_field."
            )
    return get_object_or_404(queryset, **lookup_kwargs)
def _get_object_from_date_based_view_validation(request, *args, **kwargs):
    if 'queryset' not in kwargs:
        return False
    elif 'year' not in kwargs or 'month' not in kwargs or 'day' not in kwargs:
        return False
    elif 'object_id' not in kwargs and 'slug' not in kwargs:
        return False
    return True
get_object_from_date_based_view.validate = \
        _get_object_from_date_based_view_validation
