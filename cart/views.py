from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.serializers import CartSerializer, CartDetailSerializer
from core.models import Cart


class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailListView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            self.queryset.filter(user=self.request.user)
                .order_by("id")
        )
