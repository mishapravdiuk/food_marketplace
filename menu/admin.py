from django.contrib import admin
from .models import Category, FoodItem

# Register your models here.


class CustomCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    save_as=True
    save_on_top=True
    list_display = ('category_name', 'vendor', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_display_links = ('category_name',)
    search_fields = ('category_name', 'slug', 'vendor__vendor_name')
    fields = ('category_name', 'vendor', 'slug', 'description', )


class CustomFoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    save_as=True
    save_on_top=True
    list_display = ('food_title', 'category', 'vendor', 'is_available')
    ordering = ('-created_at',)
    list_display_links = ('food_title', )
    search_fields = ('food_title', 'slug')
    fields = ('food_title', 'vendor', 'category', 'slug', 'price', 'description', 'image',  'is_available')

admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(FoodItem, CustomFoodItemAdmin)
