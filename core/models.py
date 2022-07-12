from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=8)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    delivery_time_days = models.IntegerField(null=True)
    active = models.BooleanField(default=0)

    def get_sizes(self):
        sizes = {}
        for size in self.sizes.all():
            sizes[size.size] = size.available_items
        return sizes

    def get_images(self):
        return [image.image for image in self.images.all()]


class ProductImage(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='products/images/')


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='sizes')
    size = models.CharField(max_length=5)
    available_items = models.IntegerField(default=0)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                blank=True)
    product_size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL,
                                     null=True)
    quantity = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_items(self):
        return [order_item for order_item in self.order_items.all()]


class OrderItemStatus:
    ordered = 'Ordered'
    returned = 'Returned'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=255, default=OrderItemStatus.ordered)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
