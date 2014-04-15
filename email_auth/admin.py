# -*- coding=utf8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, UserCreationForm, UserChangeForm
from django import forms

from models import User
from shopping_cart.models import Contact, Record


# inlines
class ContactInline(admin.TabularInline):
    model = Contact

class RecordInline(admin.TabularInline):
    model = Record
    extra = 0
    has_add_permission = has_delete_permission = lambda *args: False

UserAdmin.inlines = (ContactInline, RecordInline)


# detail view
UserAdmin.fieldsets = (
    (None, {'fields': ('email', 'password')}),
)

# create view
UserAdmin.add_fieldsets = (
    (None, {'fields': ('email', 'password1', 'password2')}),
)

# list view
UserAdmin.ordering = ()
UserAdmin.actions = None
UserAdmin.list_display = ('email', 'last_login', 'date_joined', 'is_staff', 'is_active')
UserAdmin.list_filter = ('is_staff','is_active')

# form
del UserChangeForm.declared_fields['username'], UserChangeForm.base_fields['username'], UserChangeForm.Meta.fields

del UserCreationForm.declared_fields['username'], UserCreationForm.base_fields['username'], UserCreationForm.clean_username, UserCreationForm.Meta.fields
UserCreationForm.Meta.model = User

UserAdmin.form = UserChangeForm
UserAdmin.add_form = UserCreationForm

# register
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
