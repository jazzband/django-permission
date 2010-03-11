========
Overview
========

.. warning::

    django-permissions is in alpha state. Please consider the API as supposed 
    to be changed until it reaches beta state.

What is it?
===========

django-permissions provides generic per-object permissions for Django.

How does it work?
=================

Create a new permission
-----------------------

.. code-block:: python

    from permissions.utils import register_permission
    permission = register_permission("View", "view")

Create a new group
------------------

.. code-block:: python

    from permissions.utils import register_group
    brights = register_group("Brights")
    
This will create a default Django group.

Create a FlatPage
-----------------

.. code-block:: python

    from django.contrib.flatpages.models import FlatPage
    content = FlatPage.objects.create(title="Example", url="example")

Grant permission
----------------

.. code-block:: python

    from permission.utils import grant_permission
    grant_permission("view", brights, content)

Now all users which are member of the group "Brights" have the permission to
view object "content". You can also grant permission to single users.

Check permission
----------------

.. code-block:: python

    from permission.utils import has_permission
    result = has_permission("view", request.user, content)

    if result == False:
        print "Alert!"

This will check whether the current user has the permission "View" for the 
FlatPage "content"