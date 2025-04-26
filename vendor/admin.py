from django.contrib import admin
from .models import Vendor, Category, FoodItem,OpeningHours

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display= ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links= ('user', 'vendor_name')
    list_editable= ('is_approved',)

admin.site.register(Vendor, VendorAdmin)

class  CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('category_name',)}
    list_display= ('category_name', 'vendor', 'updated_at')
    search_fields=('category_name', 'vendor__vendor_name')

admin.site.register(Category, CategoryAdmin)

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields= ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter=('is_available',)

admin.site.register(FoodItem, FoodItemAdmin)

class OpeningHoursAdmin(admin.ModelAdmin):
    list_display= ('vendor', 'day', 'from_hour', 'to_hour')
admin.site.register(OpeningHours, OpeningHoursAdmin)