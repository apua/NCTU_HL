# -*- coding=utf8 -*-


from django.db import models


class Product(models.Model):
    name = models.CharField( max_length=30 )
    price = models.SmallIntegerField()
    picture = models.ImageField( upload_to='./upload' )
    desciption = models.TextField()
    expiration = models.SmallIntegerField()



