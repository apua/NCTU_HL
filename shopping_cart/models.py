# -*- coding=utf8 -*-


from django.db import models
from django.core.validators import RegexValidator 


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.PositiveSmallIntegerField()
    picture = models.ImageField(upload_to='.')
    desciption = models.TextField()
    expiration = models.PositiveSmallIntegerField()


class Record(models.Model):
    user = models.ForeignKey('auth.User')
    product = models.ForeignKey('shopping_cart.Product')
    amount = models.PositiveSmallIntegerField()
    class Meta:
        unique_together = ('user', 'product')


class Contact(models.Model):
    user = models.OneToOneField('auth.User', primary_key=True)
    dorm = models.PositiveSmallIntegerField(
        choices=(
            ( 0, u'外宿'),
            (85, u'竹軒'),
            (88, u'女二'),
            (77, u'七舍'),
            (78, u'八舍'),
            (79, u'九舍'),
            (80, u'十舍'),
            (81, u'11舍'),
            (82, u'12舍'),
            (83, u'13舍'),
            (84, u'研一'),
            (87, u'研二'),
        ),
        )
    room = models.CharField(
        max_length=3,
        validators=[
            RegexValidator(
                r'^\d{3}$',
                u'Please enter room number with 3 digits',
                'invalid room number'
                ),
            ],
        )
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^(?:\+|\(\d+\))?[\d\- .]+$', # +886987774141 or (07)7935560 or 07-7935560
                u'Please enter phone number',
                'invalid phone number'
                ),
            ],
        )
