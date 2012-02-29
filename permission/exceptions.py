# vim: set fileencoding=utf-8 :
"""
Exceptions used in this app.

Exception:
    ValidationError
        raise when the passed permission handler is not valid.

    PermissinDetectionError
        raise when the app could not detect the permission from string.

    AlreadyRegistered
        raise when the handler of model is already registered in registry.

    NotRegistered
        raise when the handler of model is not registered in registry.


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

class ValidationError(Exception):
    """Validation error"""

class PermissionDetectionError(Exception):
    """Permission detection error"""

class AlreadyRegistered(Exception):
    """PermissionHandler of the model is already registered error"""
    def __init__(self, model):
        msg = 'Permission handler of the model "%s.%s" is already registered'
        msg = msg % (model._meta.app_label, model.__class__.__name__)
        super(AlreadyRegistered, self).__init__(msg)

class NotRegistered(Exception):
    """PermissionHandler of the model is not registered error"""
    def __init__(self, model):
        msg = 'Permission handler of the model "%s.%s" is not registered'
        msg = msg % (model._meta.app_label, model.__class__.__name__)
        super(NotRegistered, self).__init__(msg)
