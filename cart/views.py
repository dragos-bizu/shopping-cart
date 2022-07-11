from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.helpers import CartHelper
from cart.serializers import CartSerializer, CartDetailSerializer
from core.models import Cart, ProductSize


class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        stations = Cart.objects.filter(user=request.user.id)
        serializer = CartSerializer(stations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {
            'product': request.data.get('product'),
            'product_size': request.data.get('product_size'),
            'quantity': request.data.get('quantity'),
            'user': request.user.id,
        }
        size = ProductSize.objects.get(id=request.data.get('product_size'))
        if size.available_items < request.data.get('quantity'):
            return Response({'Response': 'Not enough items in stock!'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailListView(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by("id")
    serializer_class = CartDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        cart_helper = CartHelper(self.request.user)
        cart_total_price = cart_helper.calculate_cart_price()

        return Response(status=status.HTTP_200_OK, data={
            'products': self.queryset.filter(user=self.request.user),
            'total_price': cart_total_price})
