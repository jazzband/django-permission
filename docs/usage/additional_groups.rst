=================
Additional groups
=================

.. warning::

    django-permissions is in alpha state. Please consider the API as supposed
    to be changed until it reaches beta state.

This will demonstrate how one can create special groups (per convention) and
check permissions against them even if the user has not been assigned to these
groups explicitly.

Create new permissions
----------------------

.. code-block:: python

    from permissions.utils import register_permission
    permission = register_permission("View", "view")
    permission = register_permission("Edit", "edit")

Create new groups
------------------

.. code-block:: python

    from permissions.utils import register_group
    anonymous = register_group("Anonymous")
    owner = register_group("Owner")

This will create default Django groups.

Create a content object
-----------------------

.. code-block:: python

    from django.contrib.flatpages.models import FlatPage
    content = FlatPage.objects.create(title="Example", url="example")

Grant permissions
-----------------

.. code-block:: python

    from permission.utils import grant_permission
    grant_permission("view", anonymous, content)
    grant_permission("edit", owner, content)

Now all users which are member of the special group "Anonymous" have the
permission to view the object "content". And all users which are member of the
special group "Owner" have the permission to edit the content.

Check permission
----------------

.. code-block:: python

    from permission.utils import has_permission
    from permission.utils import get_group
    
    # Every user is automatically within the Anonymous group.
    groups = [get_group("Anonymous")]
    
    # The creator of the page is also within the Owner group.
    # Note: FlatPages actually don't have a creator attribute.
    if request.user == content.creator:    
        groups.append(get_group("Owner"))
    
    # Passing the additional groups to has_permission    
    result = has_permission("edit", request.user, content, groups)

    if result == False:
        print "Alert!"
