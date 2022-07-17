from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.views import token
from core.models import Order, OrderItems, ProductSize, UserProfile, \
    OrderItemStatus
from order.serializers import OrderSerializer


class OrderAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description='return user orders',
                         manual_parameters=[token],
                         responses={200: OrderSerializer})
    def get(self, request):
        order = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


order_item_id = openapi.Parameter('order_item_id', in_=openapi.IN_QUERY,
                                  type=openapi.TYPE_INTEGER)


class OrderReturnAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description='return an item',
                         manual_parameters=[token, order_item_id],
                         responses={200: 'Item returned succesfully'})
    def post(self, request):
        order_item = OrderItems.objects.get(
            id=request.data.get('order_item_id'))

        if not order_item:
            return Response({'Response': 'Item not found'},
                            status=status.HTTP_404_NOT_FOUND)

        if order_item.status == OrderItemStatus.returned:
            return Response({'Response': 'Item already returned'},
                            status=status.HTTP_400_BAD_REQUEST)

        product_size = ProductSize.objects.get(id=order_item.product_size_id)
        product_size.available_items += order_item.quantity
        product_size.save()

        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.wallet += order_item.product.price * order_item.quantity
        user_profile.save()

        order_item.status = OrderItemStatus.returned
        order_item.save()

        return Response({'Response': 'Item returned succesfully'},
                        status=status.HTTP_200_OK)
