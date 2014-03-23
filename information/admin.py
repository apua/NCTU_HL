# -*- coding=utf8 -*-


from django.contrib import admin
from information.models import Information, Schedule


#class ScheduleInline(admin.TabularInline):
class ScheduleInline(admin.StackedInline):
    model = Schedule


class InfoAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]


admin.site.register(Information, InfoAdmin)
