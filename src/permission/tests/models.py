# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField('title', max_length=200)
    content = models.TextField('content')

    author = models.ForeignKey(User, null=True,
            related_name='permission_test_articles_author')
    editor = models.ForeignKey(User, null=True,
            related_name='permission_test_articles_editor')
    authors = models.ManyToManyField(User,
            related_name='permission_test_articles_authors')
    editors = models.ManyToManyField(User,
            related_name='permission_test_articles_editors')

    created_at = models.DateTimeField('created_at', auto_now_add=True)


    class Meta:
        app_label = 'permission'

    def __unicode__(self):
        return self.title
