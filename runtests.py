#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
Run Django Test with Python setuptools test command


REFERENCE:
    http://gremu.net/blog/2010/enable-setuppy-test-your-django-apps/

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
import os, sys
try:
    import cProfile as profile
except ImportError:
    import profile

os.environ['DJANGO_SETTINGS_MODULE'] = 'miniblog.settings'
pack_dir = os.path.dirname(__file__)
test_dir = os.path.join(pack_dir, 'tests', 'src')
sys.path.insert(0, pack_dir)
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings

def runtests(verbosity=1, interactive=True):
    """Run Django Test"""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
            verbosity=verbosity, interactive=interactive, failfast=False)
    app_tests = [
            'permission'
        ]
    p = profile.Profile()
    p.runctx('test_runner.run_tests(app_tests)',{
        'test_runner': test_runner, 
        'app_tests': app_tests}, None)
    p.dump_stats('profile')
    sys.exit(None)

if __name__ == '__main__':
    runtests()

