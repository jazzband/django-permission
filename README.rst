django-permissions
==========================
.. image:: https://secure.travis-ci.org/lambdalisue/django-permission.png?branch=develop
    :target: http://travis-ci.org/lambdalisue/django-permission

An enhanced permission library which enable *handler based permission system*
to handle complex permissions in Django.

It is developed based on authentication backend system introduced from django
1.2.

Documentation
-------------
http://django-permission.readthedocs.org/en/latest/

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

3.  Follow the instruction below to apply logical permissions to django models

Apply logical permission
~~~~~~~~~~~~~~~~~~~~~~~~~
Assume you have an article model which has ``author`` attribute to store who
creat the article and you want to give the author full controll permissions
(e.g. add, change, delete permissions).

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

That's it.
Now the following codes will work as expected

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

    assert user1.has_perm('permission.change_article') == False
    assert user1.has_perm('permission.change_article', art1) == True
    assert user1.has_perm('permission.change_article', art2) == False

    assert user2.has_perm('permission.delete_article') == False
    assert user2.has_perm('permission.delete_article', art1) == False
    assert user2.has_perm('permission.delete_article', art2) == True

See `source code<http://django-permission.readthedocs.org/en/latest/_modules/permission/logics/author.html#AuthorPermissionLogic>`_
to learn how this logic works.
