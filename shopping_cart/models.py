# -*- coding=utf8 -*-

from django.db import models
from django.core.validators import RegexValidator 

from phonenumberfield import CellphoneModelField


class RecordManager(models.Manager):
    def get_formset_data(self, user):
        records = {
            r.product: r.amount
            for r in Record.objects.select_related('Project').filter(user=user)
            }
        amounts = {
            p.id: {'amount': records.get(p,0), 'name': p.name, 'price': p.price}
            for p in Product.objects.filter(on_sale=True)
            }
        return amounts


class Product(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'品名')
    price = models.PositiveSmallIntegerField(verbose_name=u'價格')
    picture = models.ImageField(blank=True, upload_to='.')
    description = models.TextField(blank=True)
    expiration = models.PositiveSmallIntegerField(default=0)
    on_sale = models.BooleanField(default=True)

    def __unicode__ (self):
        return self.name

    def __str__ (self):
        return self.name

    class Meta:
        abstract = False
        verbose_name = verbose_name_plural = u'產品'

class Record(models.Model):
    user = models.ForeignKey('email_auth.User')
    product = models.ForeignKey('shopping_cart.Product')
    amount = models.PositiveSmallIntegerField(verbose_name=u'數量')
    objects = RecordManager()
    class Meta:
        unique_together = ('user', 'product')

    def __unicode__ (self):
        return self.product.name

    def __str__ (self):
        return self.product.name

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
    # phone = CellphoneModelField(
    #     max_length=15,
    #     pattern=r'^09\d{8}$',
    #     verbose_name=u'手機' )
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
        ],)
