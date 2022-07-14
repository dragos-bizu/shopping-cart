from rest_framework import serializers
from core.models import Cart
from product.serializers import ProductSerializer, ProductSizeSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    product_size = ProductSizeSerializer(many=False, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'product_size', 'quantity')
