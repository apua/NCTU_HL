# -*- coding=utf8 -*-


from django.contrib import admin
from shopping_cart.models import Product, Order


class ProductAdmin(admin.ModelAdmin): pass
class OrderAdmin(admin.ModelAdmin): pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
