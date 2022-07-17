from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.views import token
from cart.helpers import CartHelper, is_stock
from cart.serializers import CartSerializer, CartDetailSerializer
from core.models import Cart, ProductSize, Order, OrderItems, UserProfile

product = openapi.Parameter('product_id', in_=openapi.IN_QUERY,
                            type=openapi.TYPE_INTEGER)
product_size = openapi.Parameter('product_size_id', in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER)
quantity = openapi.Parameter('quantity', in_=openapi.IN_QUERY,
                             type=openapi.TYPE_INTEGER)
user = openapi.Parameter('user_id', in_=openapi.IN_QUERY,
                         type=openapi.TYPE_INTEGER)

cart_item_id = openapi.Parameter('cart_item_id', in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER)


class CartAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description='add item to cart',
                         manual_parameters=[token, product, product_size, quantity,
                                            user],
                         responses={201: 'Item added to cart'})
    def post(self, request):
        data = {
            'product': request.data.get('product'),
            'product_size': request.data.get('product_size'),
            'quantity': request.data.get('quantity'),
            'user': request.user.id,
        }
        size = ProductSize.objects.get(id=request.data.get('product_size'))
        if not is_stock(size.available_items, request.data.get('quantity')):
            return Response({'Response': 'Not enough items in stock!'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description='remove item from cart',
                         manual_parameters=[token, cart_item_id],
                         responses={204: 'Item has been deleted'})
    def delete(self, request):
        cart = Cart.objects.get(id=request.data.get('cart_item_id'))
        if not cart:
            return Response({'Response': 'Item not found!'},
                            status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response({'Response': 'Item has been deleted'},
                        status=status.HTTP_200_OK)


cart_total_price = openapi.Response('cart_total_price',
                                    type=openapi.TYPE_NUMBER)


class CartDetailListAPIView(APIView, LimitOffsetPagination):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description='return user cart items',
                         manual_parameters=[token],
                         responses={200: CartDetailSerializer})
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

    @swagger_auto_schema(operation_description='order user cart items',
                         manual_parameters=[token],
                         responses={201: 'Order successfully placed!'})

    def post(self, request, format=None):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({'Response': 'Cart is empy'},
                            status=status.HTTP_400_BAD_REQUEST)

        for cart_item in cart_items:
            product_size = ProductSize.objects.get(
                id=cart_item.product_size_id)
            if not is_stock(product_size.available_items, cart_item.quantity):
                return Response({'Response': 'Not enough items in stock'},
                                status=status.HTTP_400_BAD_REQUEST)
        user_profile = UserProfile.objects.get(user=request.user)
        cart_helper = CartHelper(request.user)

        if user_profile.wallet < cart_helper.calculate_cart_price():
            return Response({'Response': 'Not enough money!'},
                            status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user,
                                     total_price=
                                     cart_helper.cart_total_price)

        for cart_item in cart_items:
            OrderItems.objects.create(order=order,
                                      product=cart_item.product,
                                      product_size=cart_item.product_size,
                                      quantity=cart_item.quantity)

            user_profile.wallet -= cart_item.product.price * cart_item.quantity
            user_profile.save()

            product_size = ProductSize.objects.get(
                id=cart_item.product_size_id)
            product_size.available_items -= cart_item.quantity
            product_size.save()

            Cart.objects.all().delete()
        return Response({'Response': 'Order successfully placed!'},
                        status=status.HTTP_200_OK)
