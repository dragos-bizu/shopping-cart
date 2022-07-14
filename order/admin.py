from django.contrib import admin

from core.models import Order
from core.models import OrderItems

admin.site.register(Order)
admin.site.register(OrderItems)
