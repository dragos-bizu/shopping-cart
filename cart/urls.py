from django.urls import path

from cart.views import CartDetailListAPIView, CartAPIView

urlpatterns = [
    path('add/', CartAPIView.as_view()),
    path('details/', CartDetailListAPIView.as_view()),
]
