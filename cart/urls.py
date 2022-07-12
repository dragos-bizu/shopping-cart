from django.urls import path

from cart.views import CartDetailListAPIView, CartAPIView, CartCheckoutAPIView

urlpatterns = [
    path('add/', CartAPIView.as_view(), name="cart_add"),
    path('details/', CartDetailListAPIView.as_view(), name="cart_details"),
    path('checkout/', CartCheckoutAPIView.as_view()),
]
