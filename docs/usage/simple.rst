======
Simple
======

Create a new user
-----------------

.. code-block:: python

    >>> from django.contrib.auth.models import User
    >>> user = User.objects.create(username="doe")

Create a new permission
-----------------------

.. code-block:: python

    >>> from permissions.utils import register_permission
    >>> permission = register_permission("View", "view")

Create a new role
-----------------

.. code-block:: python

    >>> from permissions.utils import register_role
    >>> editor = register_role("Editor")

Assign user to role
-------------------

.. code-block:: python

    >>> editor.add_principal(user)

Create a content object
-----------------------

.. code-block:: python

    >>> from django.contrib.flatpages.models import FlatPage
    >>> content = FlatPage.objects.create(title="Example", url="example")

Grant permission
----------------

.. code-block:: python

    >>> from permissions.utils import grant_permission
    >>> grant_permission(content, editor, "view")

Now all users which are member of the role "Editor" have the permission to
view object "content".

Check permission
----------------

.. code-block:: python

    >>> from permissions.utils import has_permission
    >>> has_permission(content, user, "view")
    True

This will check whether the current user has the permission "View" for the
FlatPage "content".

More information
----------------

.. seealso::

    This is just a simple use case. Look into the :doc:`API documentation <../api>` for more.