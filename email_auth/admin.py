from django.contrib import admin
from models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from models import User
from shopping_cart.models import Contact, Record


class ContactInline(admin.TabularInline):
    model = Contact

class RecordInline(admin.TabularInline):
    model = Record
    extra = 0
    has_add_permission = has_delete_permission = lambda *args: False

# customized UserAdmin
######################

# detail view
UserAdmin.fieldsets = (
    (None, {'fields': ('email', 'password')}),
)
UserAdmin.inlines = (ContactInline, RecordInline)

# list view
UserAdmin.ordering = ()
UserAdmin.actions = None
UserAdmin.list_display = ('email', 'last_login', 'date_joined', 'is_staff')
UserAdmin.list_filter = ('is_staff',)
UserAdmin.search_fields = []

# register
##########

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
