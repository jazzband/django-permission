# vim: set fileencoding=utf-8 :
"""
Unittest module of models


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
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Entry

class EntryModelTestCase(TestCase):
    def setUp(self):
        try:
            self.admin = User.objects.get(pk=1)
        except User.DoesNotExist:
            self.admin = User.objects.create_user(
                    username='admin', email='admin@test.com', password='password')

    def test_creation(self):
        """blogs.Entry: creation works correctly"""
        entry = Entry(title='foo', body='bar')
        entry.full_clean()
        self.assertEqual(entry.title, 'foo')
        self.assertEqual(entry.body, 'bar')

        entry.save()
        entry = Entry.objects.get(pk=entry.pk)
        self.assertEqual(entry.title, 'foo')
        self.assertEqual(entry.body, 'bar')

    def test_modification(self):
        """blogs.Entry: modification works correctly"""
        entry = Entry(title='foo', body='bar')
        entry.full_clean()
        entry.save()

        entry.title = 'foofoo'
        entry.body = 'barbar'
        entry.full_clean()
        entry.save()
        entry = Entry.objects.get(pk=entry.pk)
        self.assertEqual(entry.title, 'foofoo')
        self.assertEqual(entry.body, 'barbar')

    def test_validation(self):
        """blogs.Entry: validation works correctly"""
        from django.core.exceptions import ValidationError
        entry = Entry(title='foo', body='bar')
        entry.full_clean()
        entry.save()

        entry.title = ''
        self.assertRaises(ValidationError, entry.full_clean)

        entry.body = ''
        self.assertRaises(ValidationError, entry.full_clean)

        entry.title = '*' * 100
        self.assertRaises(ValidationError, entry.full_clean)

        entry.title = '!#$%&()'
        self.assertRaises(ValidationError, entry.full_clean)

    def test_deletion(self):
        """blogs.Entry: deletion works correctly"""
        entry = Entry(title='foo', body='bar')
        entry.full_clean()
        entry.save()

        num = Entry.objects.all().count()
        entry.delete()
        self.assertEqual(Entry.objects.all().count(), num - 1)
