# -*- coding: utf-8 -*-
from django.contrib import admin

from permissions.models import (
    ObjectPermission, Permission, Role, PrincipalRoleRelation
)


class ObjectPermissionAdmin(admin.ModelAdmin):
    list_display = ('permission', 'content_type', 'content_id', 'role')
    list_filter = ('content_type', 'role',)

admin.site.register(ObjectPermission, ObjectPermissionAdmin)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename')
    search_fields = ('name', 'codename')
    list_filter = ('content_types',)

admin.site.register(Permission, PermissionAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Role, RoleAdmin)


class PrincipalRoleRelationAdmin(admin.ModelAdmin):
    list_display = ('role', 'user', 'group', 'content_type', 'content_id')
    list_filter = ('role', 'content_type',)

admin.site.register(PrincipalRoleRelation, PrincipalRoleRelationAdmin)
