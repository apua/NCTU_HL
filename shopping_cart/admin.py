# -*- coding=utf8 -*-


from django.contrib import admin
from shopping_cart.models import Product, Record, Contact


class ProductAdmin(admin.ModelAdmin): pass
class RecordAdmin(admin.ModelAdmin): pass
class ContactAdmin(admin.ModelAdmin): pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Contact, ContactAdmin)
