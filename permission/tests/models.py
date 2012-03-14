# vim: set fileencoding=utf-8 :
"""
Models for just testing


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
from django.db import models
from django.contrib.auth.models import User
from permission import registry
from permission.handlers import PermissionHandler

class Article(models.Model):
    title = models.CharField('title', max_length=200, default='No title')
    body = models.TextField('body', blank=True, default='')
    author = models.ForeignKey(User, verbose_name='user', 
            related_name='articles')
    created_at = models.DateTimeField('created_at', auto_now_add=True)

    class Meta:
        app_label = 'permission'

    def __unicode__(self):
        return self.title

class ArticlePermissionHandler(PermissionHandler):
    def has_perm(self, user_obj, perm, obj=None):
        if user_obj.is_authenticated():
            return True
        return False
registry.register(Article, ArticlePermissionHandler)
