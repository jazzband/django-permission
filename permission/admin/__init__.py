#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""
short module explanation


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
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from permission.models import Role

class PermissionRoleAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {'fields': ('name', 'codename', 'description')}),
            (_('Permissions'), {'fields': ('_permissions', 'superrole')}),
            (_('Users'), {'fields': ('_users',)}),
        )
    filter_horizontal = ('_permissions', '_users')
    list_display = ['expand', 'name', 'codename', 'add_child', 'order_link']
    list_display_links = ['name']

    def expand(self, obj):
        if not obj._subroles.all():
            return u""
        return '<a href="?superrole=%d">+</a>' % (obj.id)
    expand.allow_tags = True
    expand.short_description = 'Expand'

    def add_child(self, obj):
        return '<a href="add/?superrole=%d">+</a>' % obj.id
    add_child.allow_tags = True
    add_child.short_description = 'Add Child'

    def queryset(self, request):
        superrole =  request.GET.get('superrole')
        qs = super(PermissionRoleAdmin, self).queryset(request)

        if not superrole:
            return qs.filter(superrole__isnull=True)
        return qs

    def order_link(self, obj):
        model_type_id = ContentType.objects.get_for_model(obj.__class__).pk
        model_id = obj.pk
        kwargs = {
            "direction": "up", 
            "model_type_id": model_type_id, 
            "model_id": model_id
        }
        url_up = reverse("pages-admin-move", kwargs=kwargs)
        kwargs["direction"] = "down"
        url_down = reverse("pages-admin-move", kwargs=kwargs)
        return '<a href="%s" class="up">%s</a><a href="%s" class="down">%s</a>' % (
            url_up, 'up', url_down, 'down'
        )
    order_link.allow_tags = True
    order_link.short_description = 'Move'
    order_link.admin_order_field = 'order'

    @staticmethod
    def move_down(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            lower_model = ModelClass.objects.get(pk=model_id)
            filters = ModelClass.extra_filters(lower_model)
            filters['order__gt'] = lower_model.order
            higher_model = ModelClass.objects.filter(**filters)[0]

            lower_model.order, higher_model.order=higher_model.order, lower_model.order

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass

    @staticmethod
    def move_up(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()
            higher_model = ModelClass.objects.get(pk=model_id)

            filters = ModelClass.extra_filters(higher_model)
            filters['order__lt'] = higher_model.order
            lower_model = ModelClass.objects.filter(**filters).reverse()[0]

            lower_model.order, higher_model.order=higher_model.order, lower_model.order

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass
admin.site.register(Role, PermissionRoleAdmin)
