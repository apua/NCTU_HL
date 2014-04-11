# -*- coding=utf8 -*-

from django.db import models


class Information(models.Model):
    contact_email = models.EmailField(verbose_name=u'連絡信箱')
    last_update = models.DateTimeField(
        auto_now = True, 
        auto_now_add = True,
    )
    announce = models.TextField(verbose_name=u'公告資訊')

    # Schedule
    location = models.CharField( max_length=20, verbose_name=u'擺攤地點')
    order_st = models.DateField(verbose_name=u'網路訂購開始時間')
    order_ed = models.DateField(verbose_name=u'網路訂購結束時間')
    alter_st = models.DateField(verbose_name=u'更改訂單開始時間')
    alter_ed = models.DateField(verbose_name=u'更改訂單結束時間')
    booth_st = models.DateField(verbose_name=u'擺攤開始時間')
    booth_ed = models.DateField(verbose_name=u'擺攤結束時間')
    act_1_st = models.TimeField(verbose_name=u'擺攤時段1開始時間')
    act_1_ed = models.TimeField(verbose_name=u'擺攤時段1結束時間')
    act_2_st = models.TimeField(verbose_name=u'擺攤時段2開始時間')
    act_2_ed = models.TimeField(verbose_name=u'擺攤時段2結束時間')

    def __unicode__ (self):
        return u'活動資訊'

    class Meta:
        abstract = False
        verbose_name = verbose_name_plural = u'活動資訊'
