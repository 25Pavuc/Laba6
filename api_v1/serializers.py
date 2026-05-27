from rest_framework import serializers
from .models import Manufacturer, Medicine, Order

class ManufacturerSerializer(serializers.ModelSerializer):
    medicines_count = serializers.IntegerField(source='medicines.count', read_only=True)
    
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'phone', 'email', 'website', 'created_at', 'medicines_count']

class MedicineSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.StringRelatedField(source='manufacturer', read_only=True)
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(), source='manufacturer', write_only=True
    )
    
    class Meta:
        model = Medicine
        fields = [
            'id', 'name', 'manufacturer', 'manufacturer_name', 'manufacturer_id',
            'category', 'price', 'stock_quantity', 'expiration_date', 
            'description', 'created_at', 'updated_at'
        ]

class OrderSerializer(serializers.ModelSerializer):
    medicine_name = serializers.StringRelatedField(source='medicine', read_only=True)
    medicine_id = serializers.PrimaryKeyRelatedField(
        queryset=Medicine.objects.all(), source='medicine', write_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'medicine', 'medicine_name', 'medicine_id', 'quantity',
            'order_date', 'status', 'customer_name', 'customer_phone', 'total_price'
        ]
        read_only_fields = ['total_price']