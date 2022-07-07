from rest_framework import viewsets

from core.models import Product
from product.serializers import ProductFullSerializer


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductFullSerializer

    # 1. List all
    def get_queryset(self):
        return (
            self.queryset.all()
        )
