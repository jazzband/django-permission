# permissions import
import permissions.utils

class ObjectPermissionsBackend(object):
    """Django backend for object permissions. Needs Django 1.2.


    Use it together with the default ModelBackend like so::

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'permissions.backend.ObjectPermissionsBackend',
        )
    """
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None

    def has_permission(self, permission_codename, user, obj=None):
        """Checks whether the passed user has passed permission for passed
        object (obj).

        This should be the primary method to check wether a user has a certain
        permission.

        Parameters
        ==========

        permission
            The permission's codename which should be checked.

        user
            The user for which the permission should be checked.

        obj
            The object for which the permission should be checked.
        """
        return permissions.utils.has_permission(obj, permission_codename, user)