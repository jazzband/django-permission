# vim: set fileencoding=utf-8 :
"""
Utilities for testing


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

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
from django.test import Client
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.sessions.middleware import SessionMiddleware

class MockRequestClient(Client):
    """
    A ``django.test.Client`` subclass which can return mock
    ``HttpRequest`` objects.
    
    """
    def request(self, **request):
        """
        Rather than issuing a request and returning the response, this
        simply constructs an ``HttpRequest`` object and returns it.
        
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REMOTE_ADDR': '127.0.0.1',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1,0),
            'wsgi.url_scheme': 'http',
            'wsgi.errors': self.errors,
            'wsgi.multiprocess':True,
            'wsgi.multithread': False,
            'wsgi.run_once': False,
            'wsgi.input': None,
            }
        environ.update(self.defaults)
        environ.update(request)
        request = WSGIRequest(environ)

        # We have to manually add a session since we'll be bypassing
        # the middleware chain.
        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        return request


def mock_request():
    """
    Construct and return a mock ``HttpRequest`` object; this is used
    in testing backend methods which expect an ``HttpRequest`` but
    which are not being called from views.
    
    """
    return MockRequestClient().request()

def create_user(username):
    from django.contrib.auth.models import User
    user = User.objects.create_user(
            username=username,
            email='%s@test.com'%username,
            password='password'
        )
    return user

def create_role(name):
    from permission.models import Role
    role = Role.objects.create(
            name=name, codename=name, description=name,
        )
    return role

def create_permission(name):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from permission.models import Role
    ct = ContentType.objects.get_for_model(Role)
    permission = Permission.objects.create(
            name=name, codename=name,
            content_type=ct
        )
    return permission
