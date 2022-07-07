from django.contrib import admin

from core.models import Product, ProductImage, ProductSize

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSize)
