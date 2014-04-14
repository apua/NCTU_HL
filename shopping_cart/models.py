# -*- coding=utf8 -*-

from django.db import models
from django.core.validators import RegexValidator 


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.PositiveSmallIntegerField()
    picture = models.ImageField(blank=True, upload_to='.')
    description = models.TextField(blank=True)
    expiration = models.PositiveSmallIntegerField(default=0)
    on_sale = models.BooleanField(default=True)

    def __unicode__ (self):
        return self.name

    class Meta:
        abstract = False
        verbose_name = verbose_name_plural = u'產品'

class Record(models.Model):
    user = models.ForeignKey('email_auth.User')
    product = models.ForeignKey('shopping_cart.Product')
    amount = models.PositiveSmallIntegerField()
    class Meta:
        unique_together = ('user', 'product')


class Contact(models.Model):
    user = models.OneToOneField('email_auth.User', primary_key=True)
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
        verbose_name=u'宿舍' )
    room = models.CharField(
        max_length=3,
        validators=[
            RegexValidator(
                r'^\d{3}$',
                #u'Please enter room number with 3 digits',
                u'請輸入 3 位數字的房號',
                #u'invalid phone number'
                u'房號不符合格式'
                ),
            ],
        verbose_name=u'房號' )
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                #r'^(?:\+|\(\d+\))?[\d\- .]+$', # +886987774141 or (07)7935560 or 07-7935560
                r'^09\d{8}$', #09aabbbccc
                #u'Please enter phone number',
                u'請輸入手機號碼',
                #u'invalid phone number'
                u'invalid phone number'
                ),
            ],
        verbose_name=u'手機' )
