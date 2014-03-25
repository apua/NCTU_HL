# -*- coding=utf8 -*-


from django.contrib import admin
from information.models import Information


class InfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Information, InfoAdmin)
