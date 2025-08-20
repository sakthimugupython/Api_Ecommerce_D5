from rest_framework import serializers
from .models import Customer, Product, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_number']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock_quantity']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )
    products = serializers.StringRelatedField(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, write_only=True, source='products'
    )

    class Meta:
        model = Order
        fields = [
            'id', 'order_date', 'status',
            'customer', 'customer_id',
            'products', 'product_ids'
        ]

    def create(self, validated_data):
        products = validated_data.pop('products', [])
        order = Order.objects.create(**validated_data)
        order.products.set(products)
        return order

    def update(self, instance, validated_data):
        products = validated_data.pop('products', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if products is not None:
            instance.products.set(products)
        return instance
