# -*- coding=utf8 -*-

from django.contrib import admin
from information.models import Information as Info


class InfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

admin.site.register(Info, InfoAdmin)
