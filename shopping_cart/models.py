# -*- coding=utf8 -*-


from django.db import models


class Product(models.Model):
    name = models.CharField( max_length=30 )
    price = models.SmallIntegerField()
    picture = models.ImageField( upload_to='./upload' )
    desciption = models.TextField()
    expiration = models.SmallIntegerField()


class Record(models.Model):
    user = models.ForeignKey('auth.User')
    product = models.ForeignKey('shopping_cart.Product')
    amount = models.SmallIntegerField()
    class Meta:
        unique_together = ('user', 'product')
