# -*- coding=utf8 -*-


from django.contrib import admin
from shopping_cart.models import Product


class ProductAdmin(admin.ModelAdmin): pass


admin.site.register(Product, ProductAdmin)
