from django.urls import path

from order.views import OrderAPIView

urlpatterns = [
    path('', OrderAPIView.as_view())
]
