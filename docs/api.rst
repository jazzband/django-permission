===
API
===

.. automodule:: permissions.utils

Utils
=====

Manage permissions
------------------

  .. autofunction:: grant_permission
  .. autofunction:: remove_permission
  .. autofunction:: has_permission
  .. autofunction:: reset

Manage roles
------------

  .. autofunction:: add_role
  .. autofunction:: add_local_role
  
  .. autofunction:: get_roles
  .. autofunction:: get_global_roles
  .. autofunction:: get_local_roles
  
  .. autofunction:: remove_role
  .. autofunction:: remove_local_role
  
  .. autofunction:: remove_roles
  .. autofunction:: remove_local_roles
  
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

Register roles
^^^^^^^^^^^^^^

  .. autofunction:: register_role
  .. autofunction:: unregister_role

Register groups
^^^^^^^^^^^^^^^

  .. autofunction:: register_group
  .. autofunction:: unregister_group

Helpers 
-------

  .. autofunction:: get_user
  .. autofunction:: get_group
  .. autofunction:: get_role

Template tags
=============

**ifhasperm**

Checks whether the current user has passed permission::

    {% ifhasperm view %}
        <span>Has permission</span>
    {% else %}
        <span>Doesn't have permission</span>
    {% endifhasperm %}

Models
======

.. autoclass:: permissions.PermissionBase
    :members:

.. autoclass:: permissions.models.Permission
    :members:

.. autoclass:: permissions.models.ObjectPermission
    :members:

.. autoclass:: permissions.models.ObjectPermissionInheritanceBlock
    :members:

.. autoclass:: permissions.models.Role
    :members:

.. autoclass:: permissions.models.PrincipalRoleRelation
    :members:
