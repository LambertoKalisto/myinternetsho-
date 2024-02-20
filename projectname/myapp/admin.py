from django.contrib import admin
from .models import Product, Order, Category, Cart

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_filter = ['category']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
# admin.site.register(Cart)
class OrderItemAdmin(admin.TabularInline):
    model = Cart
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    inlines = [OrderItemAdmin]