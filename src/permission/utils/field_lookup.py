# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from permission.compat import isiterable


def field_lookup(obj, field_path):
    """
    Lookup django model field in similar way of django query lookup

    Args:
        obj (instance): Django Model instance
        field_path (str): '__' separated field path

    Example:
        >>> from django.db import model
        >>> from django.contrib.auth.models import User
        >>> class Article(models.Model):
        >>>     title = models.CharField('title', max_length=200)
        >>>     author = models.ForeignKey(User, null=True,
        >>>             related_name='permission_test_articles_author')
        >>>     editors = models.ManyToManyField(User,
        >>>             related_name='permission_test_articles_editors')
        >>> user = User.objects.create_user('test_user', 'password')
        >>> article = Article.objects.create(title='test_article',
        ...                                  author=user)
        >>> aritcle.editors.add(user)
        >>> assert 'test_article' == field_lookup(article, 'title')
        >>> assert 'test_user' == field_lookup(article, 'user__username')
        >>> assert ['test_user'] == list(field_lookup(article,
        ...                                           'editors__username'))
    """
    if hasattr(obj, 'iterator'):
        return (field_lookup(x, field_path) for x in obj.iterator())
    elif isiterable(obj):
        return (field_lookup(x, field_path) for x in iter(obj))
    # split the path
    field_path = field_path.split("__", 1)
    if len(field_path) == 1:
        return getattr(obj, field_path[0], None)
    return field_lookup(field_lookup(obj, field_path[0]), field_path[1])
