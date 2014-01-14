#!/usr/bin/env python
# coding: utf-8
"""
Run Django Test with Python setuptools test command

References
----------
-   http://gremu.net/blog/2010/enable-setuppy-test-your-django-apps/
"""   
import os, sys
try:
    import cProfile as profile
except ImportError:
    import profile

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
test_dir = os.path.join(os.path.dirname(__file__), 'tests')
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
    p.dump_stats('.profile')
    sys.exit(None)

if __name__ == '__main__':
    runtests()
