# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'


def create_user(username):
    from django.contrib.auth.models import User
    user = User.objects.create_user(
            username=username,
            email="%s@test.com" % username,
            password="password"
        )
    return user

def create_article(title, user=None):
    import datetime
    from permission.tests.models import Article
    user = user or create_user(str(datetime.datetime.now()))
    article = Article.objects.create(
            title=title,
            content=title*20,
            author=user)
    return article

def create_permission(name, model=None):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from permission.tests.models import Article
    model = model or Article
    ct = ContentType.objects.get_for_model(model)
    permission = Permission.objects.create(
            name=name, codename=name,
            content_type=ct
        )
    return permission
