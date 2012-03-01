# vim: set fileencoding=utf-8 :
"""
Admin


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
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from permission.models import Role

if 'feincms' in settings.INSTALLED_APPS:
    from mptt.admin import FeinCMSModelAdmin as ModelAdmin
else:
    from mptt.admin import MPTTModelAdmin as ModelAdmin

# SimpleListFilter is only available with Django dev version.
#class PermissionListFilter(admin.SimpleListFilter):
#    title = _('permission')
#
#    parameter_name = 'permission'
#
#    def lookups(self, request, model_admin):
#        return (
#            ('view', _('View permissions')),
#            ('add', _('Add permissions')),
#            ('change', _('Change permissions')),
#            ('delete', _('Delete permissions')),
#            ('others', _('Other permissions')),
#        )
#    def queryset(self, request, queryset):
#        if self.value() == 'others':
#            qs = queryset.exclude(_permissions__codename__istartswith='view')
#            qs = qs.exclude(_permissions__codename__istartswith='add')
#            qs = qs.exclude(_permissions__codename__istartswith='change')
#            qs = qs.exclude(_permissions__codename__istartswith='delete')
#            return qs
#        else:
#            qs = queryset.filter(_permissions__codename__istartswith=self.value())
#            return qs

class PermissionRoleAdmin(ModelAdmin):
    fieldsets = (
            (None, {'fields': ('name', 'codename', 'description')}),
            (_('Roles'), {'fields': ('parent',)}),
            (_('Permissions'), {'fields': ((
                '_permissions', 'list_of_permissions', 'inherited_permissions'),)}),
            (_('Users'), {'fields': (('_users', 'list_of_users', 'inherited_users'),)}),
        )
    filter_horizontal = ('_permissions', '_users',)
    list_display = ('name', 'codename', 'description',)
    list_filter = ('_permissions__codename',)
    readonly_fields = (
            'children_roles', 
            'list_of_permissions', 'list_of_users',
            'inherited_permissions', 'inherited_users',)
    search_fields = (
            'codename', '_permissions__app_label', '_permissions__codename', 
            '_users__username', '_users__email'
        )
    
    def children_roles(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        roles = obj.get_descendants()
        for role in roles.iterator():
            row.append(li % role)
        return ul % "\n".join(row)
    children_roles.allow_tags = True
    children_roles.short_description = _('Children roles')

    def inherited_permissions(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        self_permission_pks = obj._permissions.values_list('id', flat=True)
        permissions = obj.permissions.exclude(pk__in=self_permission_pks)
        for perm in permissions.iterator():
            row.append(li % perm)
        return ul % "\n".join(row)
    inherited_permissions.allow_tags = True
    inherited_permissions.short_description = _('Inherited permissions')

    def inherited_users(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        self_permission_pks = obj._users.values_list('id', flat=True)
        users = obj.users.exclude(pk__in=self_permission_pks)
        for perm in users.iterator():
            row.append(li % perm)
        return ul % "\n".join(row)
    inherited_users.allow_tags = True
    inherited_users.short_description = _('Inherited users')

    def list_of_permissions(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        permissions = obj.permissions
        for perm in permissions.iterator():
            row.append(li % perm)
        return ul % "\n".join(row)
    list_of_permissions.allow_tags = True
    list_of_permissions.short_description = _('Current permissions')

    def list_of_users(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        users = obj.users
        for perm in users.iterator():
            row.append(li % perm)
        return ul % "\n".join(row)
    list_of_users.allow_tags = True
    list_of_users.short_description = _('Current users')

admin.site.register(Role, PermissionRoleAdmin)
