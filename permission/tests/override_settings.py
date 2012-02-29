from __future__ import with_statement
import copy
from django.conf import settings, UserSettingsHolder
from django.utils.functional import wraps

SETTING_DELETED = object()

# Backported from Django trunk (r16377)
class override_settings(object):
    """
    Temporarily override Django settings.

    Acts as either a decorator, or a context manager.  If it's a decorator it
    takes a function and returns a wrapped function.  If it's a contextmanager
    it's used with the ``with`` statement.  In either event entering/exiting
    are called before and after, respectively, the function/block is executed.
    """
    def __init__(self, **kwargs):
        self.options = kwargs
        self.wrapped = settings._wrapped
        self._resyncdb = False

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def __call__(self, test_func):
        from django.test import TransactionTestCase
        if isinstance(test_func, type) and issubclass(test_func, TransactionTestCase):
            # When decorating a class, we need to construct a new class
            # with the same name so that the test discovery tools can
            # get a useful name.
            def _pre_setup(innerself):
                self.enable()
                test_func._pre_setup(innerself)
            def _post_teardown(innerself):
                test_func._post_teardown(innerself)
                self.disable()
            inner = type(
                test_func.__name__,
                (test_func,),
                {
                    '_pre_setup': _pre_setup,
                    '_post_teardown': _post_teardown,
                    '__module__': test_func.__module__,
                })
        else:
            @wraps(test_func)
            def inner(*args, **kwargs):
                with self:
                    return test_func(*args, **kwargs)
        return inner

    def enable(self):
        class OverrideSettingsHolder(UserSettingsHolder):
            def __getattr__(self, name):
                if name == "default_settings":
                    return self.__dict__["default_settings"]
                return getattr(self.default_settings, name)

        override = OverrideSettingsHolder(copy.copy(settings._wrapped))
        for key, new_value in self.options.iteritems():
            if new_value is SETTING_DELETED:
                try:
                    delattr(override.default_settings, key)
                except AttributeError:
                    pass
            else:
                setattr(override, key, new_value)
        settings._wrapped = override

        original_apps = frozenset(getattr(self.wrapped, 'INSTALLED_APPS'))
        override_apps = frozenset(getattr(override, 'INSTALLED_APPS'))
        if original_apps != override_apps:
            # is new app in override_apps?
            def new_app_exists():
                for app in override_apps:
                    if app not in original_apps:
                        return True
                return False
            if new_app_exists():
                # call ``syncdb`` command
                recall_syncdb()
                # clear all models meta cache if possible
                if 'django.contrib.contenttypes' in getattr(override, 'INSTALLED_APPS'):
                    clear_all_meta_caches()
                self._resyncdb = True

    def disable(self):
        settings._wrapped = self.wrapped
        if self._resyncdb:
            from django.db.models import loading
            loading.cache.loaded = False

def with_apps(*apps):
    """
    Class decorator that makes sure the passed apps are present in
    INSTALLED_APPS.
    """
    apps_set = set(settings.INSTALLED_APPS)
    apps_set.update(apps)
    return override_settings(INSTALLED_APPS=list(apps_set))

def without_apps(*apps):
    """
    Class decorator that makes sure the passed apps are not present in
    INSTALLED_APPS.
    """
    apps_list = [a for a in settings.INSTALLED_APPS if a not in apps]
    return override_settings(INSTALLED_APPS=apps_list)

def recall_syncdb():
    """call ``syncdb`` command to create tables of new app's models"""
    from django.db.models import loading
    from django.core.management import call_command
    loading.cache.loaded = False
    call_command('syncdb', interactive=False, verbosity=0, migrate=False)

def clear_meta_caches(model):
    """clear model meta caches. it is required to refresh m2m relation"""
    CACHE_NAMES = (
            '_m2m_cache', '_field_cache', '_name_map',
            '_related_objects_cache', '_related_many_to_many_cache'
        )
    for name in CACHE_NAMES:
        if hasattr(model._meta, name):
            delattr(model._meta, name)

def clear_all_meta_caches():
    """clear all models meta caches by contenttype
    
    .. Note::
        'django.contrib.contenttypes' is required to installed

    """
    from django.contrib.contenttypes.models import ContentType
    for ct in ContentType.objects.iterator():
        clear_meta_caches(ct.model_class())
