from rest_framework import viewsets

from core.models import Product
from product.serializers import ProductFullSerializer


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductFullSerializer
