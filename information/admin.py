# -*- coding=utf8 -*-

from django.contrib import admin
from information.models import Information as Info


class InfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Info.objects.all().exists():
            return False
        return True

admin.site.register(Info, InfoAdmin)
