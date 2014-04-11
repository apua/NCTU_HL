# -*- coding=utf8 -*-

import inspect

from django.contrib import admin
from django.db.models.base import ModelBase

from models import Product, Record


class RecordInline(admin.TabularInline):
    model = Record
    extra = 0
    has_add_permission = has_delete_permission = lambda *args: False

class ProductAdmin(admin.ModelAdmin):

    # detail view
    inlines = (RecordInline,)

    # list view
    list_display = ('name','get_amount')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_amount(self, obj):
        return sum(r.amount for r in Record.objects.filter(product=obj))
    get_amount.short_description = u'amount'


admin.site.register(Product, ProductAdmin)
