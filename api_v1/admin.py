from django.contrib import admin
from .models import Manufacturer, Medicine, Order

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country', 'phone', 'email']
    search_fields = ['name', 'country']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'manufacturer', 'category', 'price', 'stock_quantity']
    list_filter = ['category', 'manufacturer']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'medicine', 'quantity', 'status', 'customer_name', 'total_price']
    list_filter = ['status']