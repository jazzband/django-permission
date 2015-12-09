import django

if django.VERSION >= (1, 9):
    urlpatterns = []
else:
    try:
        from django.conf.urls import *
    except ImportError:
        from django.conf.urls.defaults import *
    urlpatterns = patterns('')


