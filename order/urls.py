from django.urls import path

from order.views import OrderAPIView, OrderReturnAPIView

urlpatterns = [
    path('', OrderAPIView.as_view()),
    path('return/', OrderReturnAPIView.as_view(), name='order_return'),
]
