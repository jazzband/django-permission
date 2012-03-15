# vim: set fileencoding=utf-8 :
"""
PermissionHandler registry


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
License:
    The MIT License (MIT)

    Copyright (c) 2012 Alisue allright reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.

"""
from __future__ import with_statement
from django.conf import settings
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured

from permission.exceptions import AlreadyRegistered
from permission.exceptions import NotRegistered
from permission.handlers.base import PermissionHandler

__all__ = ('registry', 'PermissionHandler',)


class Registry(object):
    """Registry of permission handlers

    Register permission handlers to this registry to use.

    """
    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, handler_class):
        """register new permission handler for the model(s)

        If the model is already registered in registry,
        ``AlreadyRegistered`` exception will come up.

        """
        # Don't import the humonogus validation code unless required
        if settings.DEBUG:
            from permission.validation import validate
        else:
            validate = lambda model, mediator: None

        if not hasattr(model_or_iterable, '__iter__'):
            # this mean subclass of models.Model
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            # Validate (which might be a no-op)
            validate(handler_class, model)

            if model._meta.abstract:
                raise ImproperlyConfigured(
                        'The model %s is abstract, so it cannot be registered '
                        'with permission.' % model.__name__)
            if model in self._registry:
                raise AlreadyRegistered(model)

            # Instantiate the handler to save in the registry
            instance = handler_class(model)
            self._registry[model] = instance

    def unregister(self, model_or_iterable):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered(model)
            # remove from registry
            del self._registry[model]

    def get_handlers(self):
        return tuple(self._registry.values())

    def get_module_handlers(self, app_label):
        return tuple()

registry = Registry()
