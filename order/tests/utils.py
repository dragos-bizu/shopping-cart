from core.models import Order, OrderItems


def create_sample_order(user):
    return Order.objects.create(user=user)


def create_sample_order_item(order, product, product_size, quantity):
    return OrderItems.objects.create(order=order, product=product,
                                     product_size=product_size,
                                     quantity=quantity)
