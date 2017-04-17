=================
Additional groups
=================

This will demonstrate how one can create special groups (per convention) and
check permissions against them even if the user has not been assigned to these
groups explicitly.

Create a new user
-----------------

.. code-block:: python

    >>> from django.contrib.auth.models import User
    >>> user = User.objects.create(username="doe")

Create new permissions
----------------------

.. code-block:: python

    >>> from permissions.utils import register_permission
    >>> permission = register_permission("View", "view")
    >>> permission = register_permission("Edit", "edit")

Create new role
---------------

.. code-block:: python

    >>> from permissions.utils import register_role
    >>> anonymous = register_role("Anonymous")
    >>> owner = register_role("Owner")

This will create default Django groups.

Create a content object
-----------------------

.. code-block:: python

    >>> from django.contrib.flatpages.models import FlatPage
    >>> content = FlatPage.objects.create(title="Example", url="example")
    >>> content.creator = user

Grant permissions
-----------------

.. code-block:: python

    >>> from permissions.utils import grant_permission
    >>> grant_permission(content, anonymous, "view")
    >>> grant_permission(content, owner, "edit")

Now all users which are member of the special group "Anonymous" have the
permission to view the object "content". And all users which are member of the
special group "Owner" have the permission to edit the content.

Check permission
----------------

.. code-block:: python

    >>> from permissions.utils import has_permission

    # Every user is automatically within the Anonymous group.
    >>> roles = [anonymous]

    # The creator of the page is also within the Owner group.
    # Note: FlatPages actually don't have a creator attribute.
    >>> if user == content.creator:
    ...    roles.append(owner)

    # Passing the additional groups to has_permission
    >>> has_permission(content, user, "edit", roles)
    True

    >>> has_permission(content, user, "view", roles)
    True

More information
----------------

.. seealso::

    This is just a simple use case. Look into the :doc:`API documentation <../api>` for more.