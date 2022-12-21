from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    save_as=True
    save_on_top=True
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    fields = ('email', 'first_name', 'last_name', 'username', 'role', 'phone_number',  'date_joined', 'last_login', 'created_at', 'modified_date', 'is_admin', 'is_staff', 'is_active', 'is_superadmin',)
    ordering = ('-date_joined',)
    readonly_fields = ('email', 'date_joined', 'last_login', 'created_at', 'modified_date', 'is_admin', 'is_staff', 'is_active', 'is_superadmin', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)