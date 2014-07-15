#!/usr/bin/env python
# coding: utf-8
"""
Run Django Test with Python setuptools test command


REFERENCE:
    http://gremu.net/blog/2010/enable-setuppy-test-your-django-apps/

"""
import os
import sys


def parse_args():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--where', default=None)
    opts, args = parser.parse_args()
    return opts, args


def run_tests(base_dir=None, apps=None, verbosity=1, interactive=False):
    base_dir = base_dir or os.path.dirname(__file__)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    sys.path.insert(0, os.path.join(base_dir, 'src'))
    sys.path.insert(0, os.path.join(base_dir, 'tests'))

    import django
    if django.VERSION >= (1, 7):
        django.setup()

    from django.conf import settings
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity,
                             interactive=interactive, failfast=False)
    if apps:
        app_tests = [x.strip() for x in apps if x]
    else:
        app_tests = [
            'permission',
        ]
    failures = test_runner.run_tests(app_tests)
    sys.exit(bool(failures))


if __name__ == '__main__':
    opts, args = parse_args()
    run_tests(opts.where, args)
