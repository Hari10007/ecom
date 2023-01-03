from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
from .models import User, Address

# Register your models here.

class AccountAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'phone_number','date_joined','is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'fields': ('email','phone_number', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'username')
        })
    )

admin.site.register(User, AccountAdmin)
admin.site.register(Address)