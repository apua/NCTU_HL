# -*- coding=utf8 -*-


from django.db import models


class Information(models.Model):
    contact_email = models.EmailField()
    last_update = models.DateTimeField(
        auto_now = True, 
        auto_now_add = True
    )
    announce = models.TextField()


class Action(models.Model):
    info = models.OneToOneField( Information, primary_key=True)
    location = models.CharField( max_length=20 )
    order_st = models.DateField()
    order_ed = models.DateField()
    alter_st = models.DateField()
    alter_ed = models.DateField()
    booth_st = models.DateField()
    booth_ed = models.DateField()
    range1st = models.TimeField()
    range2nd = models.TimeField()
