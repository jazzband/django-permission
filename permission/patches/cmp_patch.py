# vim: set fileencoding=utf-8 :
"""
To fix ``AssertionError: Sequences differ: ...`` error in unittest.

With ``unittest2`` package or with django's bundle unittest which is
used when the version of python is under 2.7 (see ``django.utils.unittest``),
using ``assertItemsEqual`` with model list will raise ``AssertionError``.

The exception raise because when they call ``sorted(expected_seq)`` or 
``sorted(actual_seq)`` in ``assertItemsEqual`` method 
(see ``django.utils.unittest.case.py:865``), they cannot sort Model instance 
because they don't know how. 

This patch simply add ``__cmp__`` method to ``django.db.models.Model`` class
which compare its primary key (``_get_pk_val()`` method return its primary key)
if the method is not exist.


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
from django.db.models import Model

if not hasattr(Model, '__cmp__'):
    Model.__cmp__ = lambda self, other: cmp(self._get_pk_val(), other._get_pk_val())
