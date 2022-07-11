from django.urls import path, include
from rest_framework import routers

from cart.views import CartDetailListView, CartAPIView

app_name = 'cart'

router = routers.DefaultRouter()
router.register('details', CartDetailListView)

urlpatterns = [
    path('', include(router.urls)),
    path('add/', CartAPIView.as_view())
]
