from django.contrib import admin
from accounts.models import User, UserProfile
from django.contrib.auth.admin import UserAdmin


# Register your models here.



class CustomUserAdmin(UserAdmin):
    save_as=True
    save_on_top=True
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    fields = ('email', 'first_name', 'last_name', 'username', 'role', 'phone_number',  'date_joined', 'last_login', 'created_at', 'modified_date', 'is_admin', 'is_staff', 'is_active', 'is_superadmin',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'modified_date', 'is_admin', 'is_staff', 'is_active', 'is_superadmin', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display_links = ('username', 'email')


class CustomUserProfileAdmin(admin.ModelAdmin):
    save_as=True
    save_on_top=True
    list_display = ('user', 'created_at', 'modified_at',)
    ordering = ('-created_at',)
    list_display_links = ('user',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, CustomUserProfileAdmin)