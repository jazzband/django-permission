# vim: set fileencoding=utf-8 :
from setuptools import setup, find_packages

version = '0.4.6'

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="django-permission",
    version=version,
    description = "A enhanced permission system which enable object permission and role based permission",
    long_description=read('README.rst'),
    classifiers = [
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',

    ],
    keywords = "django object role permisssion auth",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/django-permission",
    download_url = r"https://github.com/lambdalisue/django-permission/tarball/master",
    license = 'MIT',
    packages = find_packages(exclude=['tests']),
    include_package_data = True,
    zip_safe=False,
    install_requires=[
        'distribute',
        'setuptools-git',
        'mock',
        'PyYAML',
        'django>=1.3',
        'django-mptt',
        'django-override-settings',
    ],
    test_suite='runtests.runtests',
    tests_require=[
        'feincms',
    ],
)
