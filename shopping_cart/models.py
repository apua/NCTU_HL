# -*- coding=utf8 -*-


from django.db import models


class Product(models.Model):
<<<<<<< local
    name = models.CharField( max_length=30 )
=======
    name = models.CharField(
        max_length=30
    )
    picture = models.ImageField(
        upload_to='./upload'
    )
>>>>>>> other
    price = models.SmallIntegerField()
<<<<<<< local
    picture = models.ImageField( upload_to='./upload' )
=======
>>>>>>> other
    desciption = models.TextField()
<<<<<<< local
    expiration = models.SmallIntegerFid()
=======
    expiration = models.SmallIntegerField()
>>>>>>> other



