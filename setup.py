# coding=utf-8
from setuptools import setup, find_packages

NAME = 'django-permission'
VERSION = '0.5.0'

def read(filename, strip=False):
    import os
    import string
    BASE_DIR = os.path.dirname(__file__)
    fi = open(os.path.join(BASE_DIR, filename), 'r')
    bu = fi.readlines()
    if strip:
        bu = [x for x in map(string.strip, bu) if x]
    fi.close()
    return bu

setup(
    name = NAME,
    version = VERSION,
    description = ('A enhanced permission system which enable logical permission'
                   'systems to complex permissions'),
    long_description = "\n".join(read('README.rst')),
    classifiers = (
        'Development Status :: 3 - Alpha',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ),
    keywords = 'django object logical permission auth authentication',
    author = 'Alisue',
    author_email = 'lambdalisue@hashnote.net',
    url = 'https://github.com/lambdalisue/%s' % NAME,
    download_url = ('https://github.com/lambdalisue/%s/'
                    'tarball/master') % NAME,
    license = 'MIT',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    exclude_package_data = {'': 'README.rst'},
    zip_safe=True,
    install_requires=read('requirements.txt', strip=True),
    test_suite='runtests.runtests',
    tests_require=read('requirements-test.txt', strip=True),
)
