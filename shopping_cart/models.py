# -*- coding=utf8 -*-


from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=30
    )
    picture = models.ImageField(
        upload_to='./upload'
    )
    price = models.IntegerField()
    desciption = models.TextField()
    expiration = models.IntegerField()



