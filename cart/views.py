from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.helpers import CartHelper
from cart.serializers import CartSerializer, CartDetailSerializer
from core.models import Cart, ProductSize, Order, OrderItems, UserProfile


class CartAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart = Cart.objects.filter(user=request.user.id)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {
            'product': request.data.get('product'),
            'product_size': request.data.get('product_size'),
            'quantity': request.data.get('quantity'),
            'user': request.user.id,
        }
        size = ProductSize.objects.get(id=request.data.get('product_size'))
        if int(size.available_items) < int(request.data.get('quantity')):
            return Response({'Response': 'Not enough items in stock!'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailListAPIView(APIView, LimitOffsetPagination):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart_products = Cart.objects.filter(user=request.user)
        cart_helper = CartHelper(request.user)
        cart_total_price = cart_helper.calculate_cart_price()

        results = self.paginate_queryset(cart_products, request, view=self)
        serializer = CartDetailSerializer(results, many=True)

        return self.get_paginated_response(
            {'products': serializer.data, 'total_price': cart_total_price})


class CartCheckoutAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({'Response': 'Cart is empy'},
                            status=status.HTTP_400_BAD_REQUEST)

        for cart_item in cart_items:
            product_size = ProductSize.objects.get(
                id=cart_item.product_size_id)
            if int(product_size.available_items) < int(cart_item.quantity):
                return Response({'Response': 'Not enough items in stock'},
                                status=status.HTTP_400_BAD_REQUEST)
        cart_helper = CartHelper(request.user)
        order = Order.objects.create(user=request.user,
                                     total_price=
                                     cart_helper.calculate_cart_price())

        for cart_item in cart_items:
            OrderItems.objects.create(order=order,
                                      product=cart_item.product,
                                      product_size=cart_item.product_size,
                                      quantity=cart_item.quantity)

            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.wallet -= cart_item.product.price * cart_item.quantity
            user_profile.save()

            product_size = ProductSize.objects.get(
                id=cart_item.product_size_id)
            product_size.available_items -= cart_item.quantity
            product_size.save()

            Cart.objects.all().delete()
        return Response({'Response': 'Order succesfully placed!'},
                        status=status.HTTP_200_OK)
