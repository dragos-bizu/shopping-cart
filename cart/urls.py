from django.urls import path, include
from rest_framework import routers

from cart.views import CartDetailListView, CartView

app_name = 'cart'

router = routers.DefaultRouter()
router.register('details', CartDetailListView)
router.register('', CartView)

urlpatterns = [
    path('', include(router.urls))
]
