# -*- coding=utf8 -*-


from django.contrib import admin
from information.models import Information, Action


#class ActionInline(admin.TabularInline):
class ActionInline(admin.StackedInline):
    model = Action


class InfoAdmin(admin.ModelAdmin):
    inlines = [ActionInline]


admin.site.register(Information, InfoAdmin)
