from core.models import Product, ProductSize, Cart


def get_product_defaults():
    return {
        'sku': '12345678',
        'price': '20.00',
        'description': 'Slim jeans',
        'delivery_time_days': '3',
        'active': 'True'
    }


def create_sample_product(name, **params):
    defaults = get_product_defaults()
    defaults.update(params)
    return Product.objects.create(name=name, **defaults)


def create_sample_product_size(product, size, available_items):
    return ProductSize.objects.create(product=product, size=size,
                                      available_items=available_items)


def create_sample_cart(user, product, product_size, quantity):
    return Cart.objects.create(user=user, product=product,
                               product_size=product_size, quantity=quantity)
