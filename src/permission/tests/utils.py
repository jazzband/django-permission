# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'


def create_user(username, **kwargs):
    from django.contrib.auth.models import User
    user = User.objects.create_user(
        username=username,
        email="%s@test.com" % username,
        password="password",
    )
    # attribute assignment
    for key, value in kwargs.items():
        user.__dict__[key] = value
    user.save()
    return user


def create_anonymous(**kwargs):
    from django.contrib.auth.models import AnonymousUser
    return AnonymousUser(**kwargs)


def create_group(name, user=None):
    from django.contrib.auth.models import Group
    group = Group.objects.create(name=name)
    if user is not None:
        user.groups.add(group)
        user.save()
    group.save()
    return group


def create_article(title, user=None, bridge=None):
    import datetime
    from permission.tests.models import Article
    user = user or create_user(str(datetime.datetime.now()))
    article = Article.objects.create(
        title=title,
        content=title*20,
        author=user,
        single_bridge=bridge
    )
    article.save()
    return article


def create_bridge(user=None, editors=None):
    import datetime
    from permission.tests.models import Bridge
    user = user or create_user(str(datetime.datetime.now()))
    editors = editors or [create_user(str(datetime.datetime.now())+str(i))
                          for i in range(2)]
    bridge = Bridge.objects.create(author=user)
    for editor in editors:
        bridge.editors.add(editor)
    bridge.save()
    return bridge


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
    permission.save()
    return permission
