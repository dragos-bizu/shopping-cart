import string

import factory.fuzzy

from core.models import Product, ProductSize

clothes_name = ['T-shirt', 'Sweater', 'Jacket', 'Coat', 'Jeans', 'Socks',
                'Shorts', 'Tracksuit', 'Vest', 'Pajamas', 'Shoes', 'Boots',
                'Skirt', 'Dress', 'Shirt']
size_names = ['XS', 'S', 'M', 'L', 'XL']


class ProductSizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSize

    product = None
    size = factory.Iterator(size_names)
    available_items = factory.fuzzy.FuzzyInteger(0, 20)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    sku = factory.fuzzy.FuzzyText(length=8, chars=string.digits)
    price = factory.fuzzy.FuzzyFloat(2.00, 100.00)
    name = factory.fuzzy.FuzzyChoice(choices=clothes_name)
    description = factory.Faker('sentence')
    delivery_time_days = factory.fuzzy.FuzzyInteger(3, 5)
    active = factory.fuzzy.FuzzyChoice(choices=[True, True, True, False])

    @factory.post_generation
    def create_product_size(self, create, extracted, **kwargs):
        if not create:
            return
        for i in range(5):
            product_size = ProductSizeFactory.create(product=self)
