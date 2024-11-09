from django.contrib import admin
from .models import Cart, Restaurant_Cart
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display=['user', 'updated_at']

admin.site.register(Cart, CartAdmin)
admin.site.register(Restaurant_Cart)