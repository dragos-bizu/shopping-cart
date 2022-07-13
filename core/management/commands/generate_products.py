from django.core.management import BaseCommand

from product import factories


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Starting generating products (it takes some time)')
        for i in range(20):
            print(str(i * 5) + '%')
            factories.ProductFactory.create_batch(size=500)
        print('The products have been generated!')
