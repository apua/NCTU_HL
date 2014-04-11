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

    has_delete_permission = lambda *args: False

    def get_amount(self, obj):
        return Record.objects.filter(product=obj).count()
    get_amount.short_description = u'amount'


admin.site.register(Product, ProductAdmin)
