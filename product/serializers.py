from rest_framework import serializers
from core.models import Product, ProductImage, ProductSize


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'


class ProductFullSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    sizes = ProductSizeSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'sku', 'price', 'name', 'description', 'delivery_time', 'active',
            'images', 'sizes')
