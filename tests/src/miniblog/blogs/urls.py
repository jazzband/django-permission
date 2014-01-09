# vim: set fileencoding=utf-8 :
"""
Mini blog URLconf


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
License:
    The MIT License (MIT)

    Copyright (c) 2012 Alisue allright reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.

"""   
from __future__ import with_statement
try:
    from django.conf.urls import patterns, include, url
except ImportError:
    # django.conf.urls.defaults were used below Django 1.6
    from django.conf.urls.defaults import patterns, include, url


import views

urlpatterns = patterns('',
    url(r'^$', views.EntryListView.as_view(), name='blogs-entry-list'),
    url(r'^create/$', views.EntryCreateView.as_view(), 
        name='blogs-entry-create'),
    url(r'^update/(?P<pk>\d+)/$', views.EntryUpdateView.as_view(), 
        name='blogs-entry-update'),
    url(r'^delete/(?P<pk>\d+)/$', views.EntryDeleteView.as_view(), 
        name='blogs-entry-delete'),
    url(r'^(?P<slug>[^/]+)/$', views.EntryDetailView.as_view(), 
        name='blogs-entry-detail'),
)
