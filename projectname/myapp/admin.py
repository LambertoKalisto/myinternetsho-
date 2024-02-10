from django.contrib import admin
from .models import Product, Order, Category, Cart

admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Cart)
class OrderItemAdmin(admin.TabularInline):
    model = Cart
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]