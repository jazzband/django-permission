# vim: set fileencoding=utf-8 :
"""
Automatically exected commands


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
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

USERNAME = 'admin'
PASSWORD = 'password'
EMAIL = 'admin@test.com'

if settings.DEBUG:
    # From http://stackoverflow.com/questions/1466827/ --
    #
    # Prevent interactive question about wanting a superuser created. (This code
    # has to go in this otherwise empty "models" module so that it gets processed by
    # the "syncdb" command during database creation.)
    #
    # Create our own test user automatically.
    def create_testuser(app, created_models, verbosity, **kwargs):
        try:
            User.objects.get(username=USERNAME)
        except User.DoesNotExist:
            if verbosity > 1:
                print '*' * 80
                print 'Creating test user -- login: %s, password: %s' % (USERNAME, PASSWORD)
                print '*' * 80
            assert User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        else:
            if verbosity > 1:
                print 'Test user already exists. -- login: %s, password: %s' % (USERNAME, PASSWORD)
    signals.post_syncdb.disconnect(
        create_superuser,
        sender=auth_models,
        dispatch_uid='django.contrib.auth.management.create_superuser')
    signals.post_syncdb.connect(create_testuser,
        sender=auth_models, dispatch_uid='common.models.create_testuser')
