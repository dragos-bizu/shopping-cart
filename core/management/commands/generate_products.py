from django.core.management import BaseCommand

from product import factories


class Command(BaseCommand):

    def handle(self, *args, **options):
        factories.ProductFactory.create_batch(size=10)
