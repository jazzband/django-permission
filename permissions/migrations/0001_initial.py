# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField(verbose_name='Content id')),
                ('content_type', models.ForeignKey(verbose_name='Content type', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectPermissionInheritanceBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField(verbose_name='Content id')),
                ('content_type', models.ForeignKey(verbose_name='Content type', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('codename', models.CharField(unique=True, max_length=100, verbose_name='Codename')),
                ('content_types', models.ManyToManyField(related_name='content_types', verbose_name='Content Types', to='contenttypes.ContentType', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrincipalRoleRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField(null=True, verbose_name='Content id', blank=True)),
                ('content_type', models.ForeignKey(verbose_name='Content type', blank=True, to='contenttypes.ContentType', null=True)),
                ('group', models.ForeignKey(verbose_name='Group', blank=True, to='auth.Group', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='principalrolerelation',
            name='role',
            field=models.ForeignKey(verbose_name='Role', to='permissions.Role'),
        ),
        migrations.AddField(
            model_name='principalrolerelation',
            name='user',
            field=models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='objectpermissioninheritanceblock',
            name='permission',
            field=models.ForeignKey(verbose_name='Permission', to='permissions.Permission'),
        ),
        migrations.AddField(
            model_name='objectpermission',
            name='permission',
            field=models.ForeignKey(verbose_name='Permission', to='permissions.Permission'),
        ),
        migrations.AddField(
            model_name='objectpermission',
            name='role',
            field=models.ForeignKey(verbose_name='Role', blank=True, to='permissions.Role', null=True),
        ),
    ]
