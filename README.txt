What is it?
===========

LFC is a Content Manangement System based on Django

Features:
=========

- Variable templates to display the content
- Variable portlets
- Multi languages (without pain)
- Bulk upload of images + automatic scaling
- WYSIWYG-Editor
- Tagging
- Commenting
- RSS Feeds
- Pluggable (Add own content types and portlets see http://pypi.python.org/pypi/lfc-blog/

Installation
=============

0. Install mercurial

   $ easy_install mercurial"

1. Get the buildout

   hg clone http://bitbucket.org/diefenbach/lfc-buildout-development/

2. Execute the buildout

   a. $ cd lfc-buildout-development
   b. $ python boostrap
   c. $ bin/buildout -v

3. Start the server

   $ bin/django runserver

4. Login

   http://localhost:8000/login/ (admin/admin)

5. Go to the management interface

   http://localhost:8000/manage/

Changes
=======

1.0 alpha 2 (2010-01-15)
------------------------

* A lot of cleanups and bugfixes
* Added middleware to traverse objects
* Added custom object manager to handle permissions (very simple yet)
* Added simple form to manage registered content types
* Added global images
* Added some docs
* Improved multi languages handling
* Improved object actions
* Improved search
* Updated german translations

1.0 alpha 1 (2010-01-10)
------------------------

* Initial public release