from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=8)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    delivery_time_days = models.IntegerField(null=True)
    active = models.BooleanField(default=0)


class ProductImage(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    available_items = models.IntegerField(default=0)
