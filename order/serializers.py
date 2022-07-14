from rest_framework import serializers

from core.models import Order, OrderItems
from product.serializers import ProductSerializer, ProductSizeSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    product_size = ProductSizeSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItems
        fields = ('id', 'product', 'product_size', 'quantity', 'status')


class OrderSerializer(serializers.ModelSerializer):
    get_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('created_at', 'get_items', 'total_price')
