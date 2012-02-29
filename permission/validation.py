#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Validation method called in ``registry.register`` method


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
from django.db import models
from django.db.models.base import ModelBase

from permission.handlers import PermissionHandler
from permission.exceptions import ValidationError

__all__ = ('validate',)

def validate(cls, model):
    """
    Does basic PermissionHandler option validation. Calls custom validation
    classmethod in the end if it is provided in cls. The signature of the 
    custom validation classmethod should be: def validate(cls, model).

    """
    # Before we can introspect models, they need to be fully loaded so that
    # inter-relations are set up correctly. We force that here.
    models.get_apps()

    # validate model class
    if not isinstance(model, ModelBase):
        # this mean the model is not subclass of models.Model
        raise ValidationError(
                'The model "%s" must be a subclass of ``models.Model``.' % model.__class__.__name__
            )

    # validate handler class
    if not issubclass(cls, PermissionHandler):
        raise ValidationError(
                'The handler "%s" must be a subclass of '
                '``fluidpermission.handlers.PermissionHandler``.' % cls.__class__.__name__
            )

    # call custom validation classmethod
    if hasattr(cls, 'validate'):
        cls.validate(model)
