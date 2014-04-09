# -*- coding=utf8 -*-

from django.contrib import admin
from information.models import Information as Info


class InfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if len( Info.objects.all() ) == 0:
            return True
        return False

admin.site.register(Info, InfoAdmin)
