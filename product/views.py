from rest_framework import viewsets

from core.models import Product
from product.serializers import ProductFullSerializer


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductFullSerializer
