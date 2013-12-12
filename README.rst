**********************************
 django-permission
**********************************

django-permission is an enhanced permission system which support object permission and role based permission system.

**Need maintainer, let me know if you are interested in**

**This is under development. The codes below may not works in the future**

**User who are using django version less than 1.5 should check this issue (https://github.com/lambdalisue/django-permission/issues/4)**

Install
==============
django-permission is in PyPI_ so::

    $ pip install django-permission

    or

    $ pip install git+git://github.com/lambdalisue/django-permission.git#egg=django-permission

Quick tutorial
============================

1.  Add ``'permission'`` to ``INSTALLED_APPS`` of your ``settings.py`` and confirm
    ''django.contrib.auth' and 'django.contrib.contenttypes' is in ``INSTALLED_APPS``

    .. Note::
        django-permission can use `django-fenicms <https://github.com/matiasb/fenics>`_ to improve
        the visual design of change_list page in django admin if available. Add 'fenicms' to
        your ``INSTALLED_APPS`` to enable AJAX sorting, adding, expanding features.

2.  Add ``'permission.backends.PermissionBackend'`` to ``AUTHENTICATION_BACKENDS``
    of your ``settings.py``. If you cannot existing settings, simply add
    following code::

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'permission.backends.RoleBackend',
            'permission.backends.PermissionBackend',
        )

3.  Add ``permissions.py`` to the directory which contains ``models.py``. And
    write following codes for starting::

        from permission import registry
        from permission import PermissionHandler

        from models import YourModel

        class YourModelPermissionHandler(PermissionHandler):
            """Permission handler class for ``YourModel``. Similar with AdminSite"""
            def has_perm(self, user_obj, perm, obj=None):
                """this is called for checking permission of the model."""
                if user_obj.is_authenticated():
                    if perm == 'yourapp.add_yourmodel':
                        # Authenticated user has add permissions of this model
                        return True
                    elif obj and obj.author == user_obj:
                        # Otherwise (change/delete) user must be an author
                        return True
                # User doesn't have permission of ``perm``
                return False

        # register this ``YourModelPermissionHandler`` with ``YourModel``
        registry.register(YourModel, YourModelPermissionHandler)

4.  ``has`` and ``of`` keyword is added to ``if`` in template. You can check permission
    as::

        {% if user has 'blog.add_entry' %}
        <p>You can add entry</p>
        {% endif %}
        {% if object and user has 'blog.change_entry' of object or user has 'blog.delete_entry' of object %}
        <!-- object is exist and user can change or delete this object. -->
        <div class="control-panel">
            {% if user has 'blog.change_entry' of object %}
            <p>You can change this entry.</p>
            {% endif %}
            {% if user has 'blog.delete_entry' of object %}
            <p>You can delete this entry.</p>
            {% endif %}
        </div>
        {% endif %}

    .. Note::
        If you don't want django-permission to replace builtin ``if`` tag, set
        ``PERMISSION_REPLATE_BUILTIN_IF`` to ``False`` in your ``settings.py``.
        Then you have to use ``{% permission %}`` templatetag as::

            {% permission user has 'blog.add_entry' %}
            <p>You can add entry</p>
            {% endpermission %}

        ``{% permission %}`` tag is exactuly same as ``{% if %}`` thus you can use
        ``{% elpermission %}`` for ``{% elif %}`` and ``{% else %}``.

5.  ``permission_required`` decorator is used for object permission checking.
    You can use the decorator as::

        from permission.decorators import permission_required

        # As class decorator
        @permission_required('auth.change_user')
        class UpdateAuthUserView(UpdateView):
            # ...

        # As method decorator
        class UpdateAuthUserView(UpdateView):
            @permission_required('auth.change_user')
            def dispatch(self, request, *args, **kwargs):
                # ...

        # As function decorator
        @permission_required('auth.change_user')
        def update_auth_user(request, *args, **kwargs):
            # ...

    see more details in document comments on
    ``permission/decorators/__init__.py``



Role?
==========

django-permission has role based permission system. visit your django admin page to create/modify roles (See the screenshots below).
The role permissions are handled with ``permission.backends.RoleBackend``.

.. image:: ./res/Screenshot_from_2013-12-12\ 16:16:16.png
    :align: center

.. image:: ./res/Screenshot_from_2013-12-12\ 16:16:23.png
    :align: center

.. Note::
    Role based permission system does not support object permission and anonymous permission.
    However these permissions are handled with Individual handler based permission backend
    (``permission.backends.PermissionBackend``)


Regulate permissions treated in PermissionHandler
==================================================================================================

``PermissionHandler`` treat all permissions related to the model registered
with in default. But sometime you may want to exclude some permissions or
include some permissions. To regulate permissions treated, use ``includes``
and ``excludes`` attributes.

``includes`` attribute is set to
``permissions.handlers.base.get_model_permissions`` function in default. That's mean
your newly created ``PermissionHandler`` will treat all permissions which related
to the model. If you want to specify permissions, set a list/tuple or a
function which have one argument. The ``PermissionHandler`` instance will be
given as first argument.

``excludes`` attribute is set to ``None`` in default. If you want to exclude
some permissions from ``includes``, set a list/tuple or a function which
treated same as the function used in ``includes``.

Example usage::

    from permission import registry
    from permission import PermissionHandler

    from models import YourModel
    from models import HisModel
    from models import HerModel

    class AppPermissionHandler(PermissionHandler):
        # this handler treat all permissions related to this app (myapp)
        includes = lambda self: self.get_all_permissions()

        # except permissions for adding models.
        excludes = (
            'myapp.add_yourmodel',
            'myapp.add_hismodel',
            'myapp.add_hermodel',
        )

        def has_perm(self, user_obj, perm, obj=None):
            codename = self.get_permission_codename()
            # permissions for adding models are excluded with
            # ``excludes`` attribute thus the code below never
            # fail.
            assert codename.startswith('add_')
            if perm.endswith('_yourmodel'):
                # All user has all permissions for ``YourModel``
                return True
            elif perm.endswith('_hismodel'):
                if user_obj.is_authenticated():
                    # only authenticated user has all permissions for ``HisModel``
                    return True
            elif perm.endswith('_hermodel'):
                if user_obj.is_staff:
                    # only staff user has all permissions for ``HerModel``
                    return True
            return False

    # you have to register the handler with the model
    # even AppPermissionHandler doesn't care about model
    registry.register(YourModel, AppPermissionHandler)
    # registry.register(HisModel, AppPermissionHandler) # or you can register with HisModel
    # registry.register(HerModel, AppPermissionHandler) # or you can register with HerModel


.. Note::
    If you use ``user.has_perm()`` method in ``has_perm()`` method of
    ``PermissionHandler``, make sure the permission is not treated with the
    handler.
