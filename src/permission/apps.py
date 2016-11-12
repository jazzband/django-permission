from django.apps import AppConfig


class PermissionConfig(AppConfig):
    name = "permission"
    verbose_name = "Permission"

    def ready(self):
        from permission.conf import settings
        if settings.PERMISSION_AUTODISCOVER_ENABLE:
            from permission.utils.autodiscover import autodiscover
            autodiscover()
