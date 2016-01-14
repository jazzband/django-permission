django-permission
==========================
.. image:: https://secure.travis-ci.org/lambdalisue/django-permission.png?branch=master
    :target: http://travis-ci.org/lambdalisue/django-permission
    :alt: Build status

.. image:: https://coveralls.io/repos/lambdalisue/django-permission/badge.png?branch=master
    :target: https://coveralls.io/r/lambdalisue/django-permission/
    :alt: Coverage

.. image:: https://requires.io/github/lambdalisue/django-permission/requirements.svg?branch=master
    :target: https://requires.io/github/lambdalisue/django-permission/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://scrutinizer-ci.com/g/lambdalisue/django-permission/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/lambdalisue/django-permission/inspections
    :alt: Inspection

.. image:: https://img.shields.io/badge/version-0.9.1-yellow.svg?style=flat-square
    :target: setup.py
    :alt: Version 0.9.2

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: LICENSE.md
    :alt: MIT License

Author
    Alisue <lambdalisue@hashnote.net>
Supported python versions
    Python 2.6, 2.7, 3.3, 3.4, 3.5
Supported django versions
    Django 1.2 - 1.9

An enhanced permission library which enables a *logic-based permission system*
to handle complex permissions in Django.

It is developed based on the authentication backend system introduced in Django
1.2. This library does support Django 1.2 and higher.


Documentation
-------------
http://django-permission.readthedocs.org/en/latest/

Installation
------------
Use pip_ like::

    $ pip install django-permission

.. _pip:  https://pypi.python.org/pypi/pip

Note that in Django 1.2 and 1.3 requires [six](https://pythonhosted.org/six/) as well.
Install it with::

    $ pip install six

Usage
-----

The following might help you to understand as well.

- Basic strategy or so on, `Issue #28 <https://github.com/lambdalisue/django-permission/issues/28>`_
- Advanced usage and examples, `Issue #26 <https://github.com/lambdalisue/django-permission/issues/26>`_

Configuration
~~~~~~~~~~~~~
1.  Add ``permission`` to the ``INSTALLED_APPS`` in your settings
    module

    .. code:: python

        INSTALLED_APPS = (
            # ...
            'permission',
        )

2.  Add our extra authorization/authentication backend

    .. code:: python

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend', # default
            'permission.backends.PermissionBackend',
        )

3.  Follow the instructions below to apply logical permissions to django models

Autodiscovery
~~~~~~~~~~~~~
This is a new feature, added in django-permission 0.6.0, and the behavior was changed in django-permission 0.6.3.
Like django's admin package, django-permission automatically discovers the ``perms.py`` in your application directory **by running ``permission.autodiscover()``**.
Additionally, if the ``perms.py`` module has a ``PERMISSION_LOGICS`` variable, django-permission automatically run the following functions to apply the permission logics.

.. code:: python

    for model, permission_logic_instance in PERMISSION_LOGICS:
        if isinstance(model, str):
            model = get_model(*model.split(".", 1))
        add_permission_logic(model, permission_logic_instance)

**Quick tutorial**

1.  Add ``import permission; permission.autodiscover()`` to your ``urls.py`` like:

    .. code:: python

        from django.conf.urls import patterns, include, url
        from django.contrib import admin

        admin.autodiscover()
        # add this line
        import permission; permission.autodiscover()

        urlpatterns = patterns('',
            url(r'^admin/', include(admin.site.urls)),
            # ...
        )

2.  Write ``perms.py`` in your application directory like:

    .. code:: python

        from permission.logics import AuthorPermissionLogic
        from permission.logics import CollaboratorsPermissionLogic

        PERMISSION_LOGICS = (
            ('your_app.Article', AuthorPermissionLogic()),
            ('your_app.Article', CollaboratorsPermissionLogic()),
        )

You can specify a different module or variable name, with ``PERMISSION_AUTODISCOVER_MODULE_NAME`` or ``PERMISSION_AUTODISCOVER_VARIABLE_NAME`` respectively.

Apply permission logic
~~~~~~~~~~~~~~~~~~~~~~~~~
Let's assume you wrote an article model which has an ``author`` attribute to store the creator of the article, and you want to give that author full control permissions
(e.g. add, change and delete permissions).

What you need to do is just applying ``permission.logics.AuthorPermissionLogic``
to the ``Article`` model like

.. code:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Article(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        author = models.ForeignKey(User)

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    # apply AuthorPermissionLogic
    from permission import add_permission_logic
    from permission.logics import AuthorPermissionLogic
    add_permission_logic(Article, AuthorPermissionLogic())


.. note::
    From django-permission version 0.8.0, you can specify related object with
    `field__name` attribute like
    `django queryset lookup <https://docs.djangoproject.com/en/1.6/topics/db/queries/#lookups-that-span-relationships>`_.
    See the working example below:

.. code:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Article(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        project = models.ForeignKey('permission.Project')

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    class Project(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        author = models.ForeignKey(User)

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    # apply AuthorPermissionLogic to Article
    from permission import add_permission_logic
    from permission.logics import AuthorPermissionLogic
    add_permission_logic(Article, AuthorPermissionLogic(
        field_name='project__author',
    ))


That's it.
Now the following codes will work as expected:


.. code:: python

    user1 = User.objects.create_user(
        username='john',
        email='john@test.com',
        password='password',
    )
    user2 = User.objects.create_user(
        username='alice',
        email='alice@test.com',
        password='password',
    )

    art1 = Article.objects.create(
        title="Article 1",
        body="foobar hogehoge",
        author=user1
    )
    art2 = Article.objects.create(
        title="Article 2",
        body="foobar hogehoge",
        author=user2
    )

    # You have to apply 'permission.add_article' to users manually because it
    # is not an object permission.
    from permission.utils.permissions import perm_to_permission
    user1.user_permissions.add(perm_to_permission('permission.add_article'))

    assert user1.has_perm('permission.add_article') == True
    assert user1.has_perm('permission.change_article') == False
    assert user1.has_perm('permission.change_article', art1) == True
    assert user1.has_perm('permission.change_article', art2) == False

    assert user2.has_perm('permission.add_article') == False
    assert user2.has_perm('permission.delete_article') == False
    assert user2.has_perm('permission.delete_article', art1) == False
    assert user2.has_perm('permission.delete_article', art2) == True

    #
    # You may also be interested in django signals to apply 'add' permissions to the
    # newly created users.
    # https://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.post_save
    #
    from django.db.models.signals.post_save
    from django.dispatch import receiver
    from permission.utils.permissions import perm_to_permission

    @receiver(post_save, sender=User)
    def apply_permissions_to_new_user(sender, instance, created, **kwargs):
        if not created:
            return
        #
        # permissions you want to apply to the newly created user
        # YOU SHOULD NOT APPLY PERMISSIONS EXCEPT PERMISSIONS FOR 'ADD'
        # in this way, the applied permissions are not object permission so
        # if you apply 'permission.change_article' then the user can change
        # any article object.
        #
        permissions = [
            'permission.add_article',
        ]
        for permission in permissions:
            # apply permission
            # perm_to_permission is a utility to convert string permission
            # to permission instance.
            instance.user_permissions.add(perm_to_permission(permission))


See http://django-permission.readthedocs.org/en/latest/_modules/permission/logics/author.html#AuthorPermissionLogic
to learn how this logic works.

Now, assume you add ``collaborators`` attribute to store collaborators
of the article and you want to give them a change permission.

What you need to do is quite simple.
Apply ``permission.logics.CollaboratorsPermissionLogic``
to the ``Article`` model as follows


.. code:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Article(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        author = models.ForeignKey(User)
        collaborators = models.ManyToManyField(User)

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    # apply AuthorPermissionLogic and CollaboratorsPermissionLogic
    from permission import add_permission_logic
    from permission.logics import AuthorPermissionLogic
    from permission.logics import CollaboratorsPermissionLogic
    add_permission_logic(Article, AuthorPermissionLogic())
    add_permission_logic(Article, CollaboratorsPermissionLogic(
        field_name='collaborators',
        any_permission=False,
        change_permission=True,
        delete_permission=False,
    ))


.. note::
    From django-permission version 0.8.0, you can specify related object with
    `field_name` attribute like
    `django queryset lookup <https://docs.djangoproject.com/en/1.6/topics/db/queries/#lookups-that-span-relationships>`_.
    See the working example below:


.. code:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Article(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        project = models.ForeignKey('permission.Project')

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    class Project(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        collaborators = models.ManyToManyField(User)

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    # apply AuthorPermissionLogic to Article
    from permission import add_permission_logic
    from permission.logics import CollaboratorsPermissionLogic
    add_permission_logic(Article, CollaboratorsPermissionLogic(
        field_name='project__collaborators',
    ))


That's it.
Now the following codes will work as expected:


.. code:: python

    user1 = User.objects.create_user(
        username='john',
        email='john@test.com',
        password='password',
    )
    user2 = User.objects.create_user(
        username='alice',
        email='alice@test.com',
        password='password',
    )

    art1 = Article.objects.create(
        title="Article 1",
        body="foobar hogehoge",
        author=user1
    )
    art1.collaborators.add(user2)

    assert user1.has_perm('permission.change_article') == False
    assert user1.has_perm('permission.change_article', art1) == True
    assert user1.has_perm('permission.delete_article', art1) == True

    assert user2.has_perm('permission.change_article') == False
    assert user2.has_perm('permission.change_article', art1) == True
    assert user2.has_perm('permission.delete_article', art1) == False


See http://django-permission.readthedocs.org/en/latest/_modules/permission/logics/collaborators.html#CollaboratorsPermissionLogic
to learn how this logic works.

There are `StaffPermissionLogic <http://django-permission.readthedocs.org/en/latest/_modules/permission/logics/staff.html#StaffPermissionLogic>`_
and `GroupInPermissionLogic <http://django-permission.readthedocs.org/en/latest/_modules/permission/logics/groupin.html#GroupInPermissionLogic>`_ 
for ``is_staff` or ``group`` based permission logic as well.

Customize permission logic
............................
Your own permission logic class must be a subclass of
``permission.logics.PermissionLogic`` and must override
``has_perm(user_obj, perm, obj=None)`` method which return boolean value.

Class, method, or function decorator
-------------------------------------
Like Django's ``permission_required`` but it can be used for object permissions
and as a class, method, or function decorator.
Also, you don't need to specify a object to this decorator for object permission.
This decorator automatically determined the object from request
(so you cannnot use this decorator for non view class/method/function but you
anyway use ``user.has_perm`` in that case).


.. code:: python

    >>> from permission.decorators import permission_required
    >>> # As class decorator
    >>> @permission_required('auth.change_user')
    >>> class UpdateAuthUserView(UpdateView):
    ...     pass
    >>> # As method decorator
    >>> class UpdateAuthUserView(UpdateView):
    ...     @permission_required('auth.change_user')
    ...     def dispatch(self, request, *args, **kwargs):
    ...         pass
    >>> # As function decorator
    >>> @permission_required('auth.change_user')
    >>> def update_auth_user(request, *args, **kwargs):
    ...     pass


Override the builtin ``if`` template tag
----------------------------------------
django-permission overrides the builtin ``if`` tag, adding two operators to handle
permissions in templates.
You can write a permission test by using ``has`` keyword, and a target object with ``of`` as below.


.. code:: html

    {% if user has 'blogs.add_article' %}
        <p>This user have 'blogs.add_article' permission</p>
    {% elif user has 'blog.change_article' of object %}
        <p>This user have 'blogs.change_article' permission of {{object}}</p>
    {% endif %}

    {# If you set 'PERMISSION_REPLACE_BUILTIN_IF = False' in settings #}
    {% permission user has 'blogs.add_article' %}
        <p>This user have 'blogs.add_article' permission</p>
    {% elpermission user has 'blog.change_article' of object %}
        <p>This user have 'blogs.change_article' permission of {{object}}</p>
    {% endpermission %}

.. note::
    From Django 1.9, users require to add `'permission.templatetags.permissionif'` to `'builtins'` option manually.
    See
    - https://docs.djangoproject.com/en/1.9/releases/1.9/#django-template-base-add-to-builtins-is-removed
    - https://docs.djangoproject.com/en/1.9/topics/templates/#module-django.template.backends.django
    Or following example:

    .. code:: python

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'builtins': ['permission.templatetags.permissionif'],
                },
            },
        ]

License
-------------------------------------------------------------------------------
The MIT License (MIT)

Copyright (c) 2015 Alisue, hashnote.net

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
