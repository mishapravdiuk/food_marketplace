from django.contrib import admin
from .models import Vendor 


class VendorAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('user', 'vendor_name', 'is_approved')
    search_fields = ('email', 'username', 'vendor_name')
    ordering = ('created_at',)
    list_display_links = ('user', 'vendor_name')



# Register your models here.
admin.site.register(Vendor, VendorAdmin)