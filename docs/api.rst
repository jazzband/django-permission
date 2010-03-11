===
API
===

.. warning::

    django-permissions is in alpha state. Please consider the API as supposed 
    to be changed until it reaches beta state.

.. automodule:: permissions.utils

Utils
=====

Manage permissions
------------------

  .. autofunction:: grant_permission
  .. autofunction:: remove_permission
  .. autofunction:: has_permission


Manage inheritance
------------------

  .. autofunction:: add_inheritance_block
  .. autofunction:: remove_inheritance_block
  .. autofunction:: is_inherited

Registration
------------

Register permissions
^^^^^^^^^^^^^^^^^^^^

  .. autofunction:: register_permission
  .. autofunction:: unregister_permission

Register groups
^^^^^^^^^^^^^^^

  .. autofunction:: register_group
  .. autofunction:: unregister_group

Models
======

This models can be found in ``permissions.models``.

.. autoclass:: permissions.models.Permission
.. autoclass:: permissions.models.ObjectPermission
.. autoclass:: permissions.models.ObjectPermissionInheritanceBlock