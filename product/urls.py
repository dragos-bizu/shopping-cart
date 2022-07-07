from django.urls import path, include
from rest_framework import routers

from product.views import ProductListView

app_name = 'products'

router = routers.DefaultRouter()
router.register('', ProductListView)

urlpatterns = [
    path('all/', include(router.urls))
]
