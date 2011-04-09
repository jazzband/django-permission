What is it?
===========

django-permissions provides per-object permissions for Django

Code
====

The code can be found on bitbucket: http://bitbucket.org/diefenbach/django-permissions/

Implementations
===============

If you want to see a comprehensive implementation of django-permissions take 
a look at the CMS `LFC <http://pypi.python.org/pypi/django-lfc>`_

Changes
=======

1.0.2 (2011-04-09)
------------------

* Bugfix: prevent to add same Users several times to a Role; issue #6 of django-workflows
* Updated Development Status to "5 - Production/Stable"

1.0.1 (2011-04-08)
------------------

* Bugfix: DatabaseErrors with Postgres; issue #5.
* Bugfix: changed order of passed parameters to has_permission; issue #6
* Bugfix: removed not needed import of "sets"; issue #8

1.0 (2010-08-24)
----------------

* First final release

1.0 beta 4 (2010-07-23)
-----------------------

* Added check_permission method to PermissionBase
* Added Unauthorized exception

1.0 beta 3 (2010-07-07)
-----------------------

* Bugfix get_users/get_groups method of class Role; issue #2
* Bugfix: check for an object before trying to add local role; issue #3
* Bugfix: registration of permissions for specific content types only

1.0 beta 2 (2010-05-17)
-----------------------

* Added license

1.0 beta 1 (2010-05-17)
-----------------------

* Bugfix has_permission. Using roles=None instead of roles=[].

1.0 alpha 4 (2010-04-16)
------------------------

* Moved PermissionBase to __init__.py

1.0 alpha 3 (2010-03-30)
------------------------

* Added roles

1.0 alpha 2 (2010-03-22)
------------------------

* Added a lot of improvements on several places

1.0 alpha 1 (2010-03-11)
------------------------

* Initial public release