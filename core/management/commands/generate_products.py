import os

from django.core.management import BaseCommand

from core.models import Product
from product import factories


class Command(BaseCommand):

    def handle(self, *args, **options):
        size = int(os.environ.get('products_quantity'))
        if Product.objects.all():
            print('Products already generated!')
        else:
            print('Starting generating products (it takes some time)')
            for i in range(10):
                print(str(i * 10) + '%')
                factories.ProductFactory.create_batch(size // 10)
            print('The products have been generated!')
