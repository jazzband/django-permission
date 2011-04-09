========
Overview
========

* django-permissions is a generic framework for per-object permissions for
  Django which is based on roles: http://en.wikipedia.org/wiki/Role-based_access_control

Permissions
===========

* Permissions are granted to roles (and only to roles) in order to allow 
  something to users or groups which have these roles.

Roles
=====

* Roles are used to grant permissions. Typical roles are *Reader*, *Manager*  
  or *Editor*.

Local Roles
===========

* Local roles are roles which are assigned to users and groups for specific 
  content objects.

Users
=====

* Users are actors which may need a permission to do something within the 
  system.
* Users can be member of several groups.
* User can have several roles, directly or via a membership to a group
  (these are considered as global).
* User can have local roles, directly or via a membership to a group. That is
  roles for a specific object.
* Users have all roles of their groups - global and local ones.
* Users have all permissions of their roles - global and local ones.

Groups
======

* Groups combines users together.
* Groups can have roles (these are considered as global).
* Groups can have local roles, that is roles for a specific object.
* Groups has all permissions of their roles - global and local ones.
* Users of a Group have the group's roles and permissions.