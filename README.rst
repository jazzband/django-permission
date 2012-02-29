**********************************
 djagno-permission
**********************************

django-permission is an enhanced permission system which support object permission.

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

2.  Add ``'permission.backends.PermissionBackend'`` to ``AUTHENTICATION_BACKENDS``
    of your ``settings.py``. If you cannot existing settings, simply add 
    following code::

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
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

How to regulate permissions used in the handler
==============================================================================================

``PermissionHandler`` care permissions related with registered model only in default. To change
this behavior, you must define ``permissions`` attribute or ``get_permissions`` methods which
return a permission string (like 'auth.add_user') list.

``get_permissions`` return the value of ``permissions`` if the attribute is defined. Otherwise it
return all permissions related to the model in default used ``get_model_permissions`` method.

The sample code below show how to handle all permissions of the app of the model in one
``PermissionHandler``::

    from permission import registry
    from permission import PermissionHandler

    from models import YourModel
    from models import HisModel
    from models import HerModel

    class AppPermissionHandler(PermissionHandler):
        def get_permissions(self):
            # ``get_app_permissions()`` method return all permissions related
            # to the app of the model.
            return self.get_app_permissions()

        def has_perm(self, user_obj, perm, obj=None):
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
    
