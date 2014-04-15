# -*- coding=utf8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm

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
    (None, {'fields': ('email', 'password')}),
)

# list view
UserAdmin.ordering = ()
UserAdmin.actions = None
<<<<<<< local
UserAdmin.list_display = ('email', 'last_login', 'date_joined', 'is_staff')
UserAdmin.list_filter = ('is_staff',)
UserAdmin.search_fields = []
=======
UserAdmin.list_display = ('email', 'last_login', 'date_joined', 'is_staff', 'is_active')
UserAdmin.list_filter = ('is_staff','is_active')

# form
class UserForm(ModelForm):
    class Meta:
        model = User

UserAdmin.form = UserForm
UserAdmin.add_form = UserForm
>>>>>>> other

# register
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
