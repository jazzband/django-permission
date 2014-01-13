django-permissions
==========================
An enhanced permission library which enable *handler based permission system*
to handle complex permissions in Django.

It is developed based on authentication backend system introduced from django
1.2.

Installation
------------
Use pip_ like::

    $ pip install "django-permissions>=0.5.0"

.. _pip:  https://pypi.python.org/pypi/pip

Usage
-----

Configuration
~~~~~~~~~~~~~
1.  Put ``permission`` into your ``INSTALLED_APPS`` at settings
    module

    .. code:: python

        INSTALLED_APPS = (
            # ...
            'permission',
        )

2.  Add extra authorization backend

    .. code:: python

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend', # default
            'permission.backends.PermissionBackend',
        )

