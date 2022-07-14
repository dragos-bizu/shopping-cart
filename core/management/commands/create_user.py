from django.contrib.auth.models import User
from django.core.management import BaseCommand

from core.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.filter(username='tim').exists():
            print('User already created')
        else:
            user = User.objects.create(username='tim', password='tim12345')
            UserProfile.objects.create(user=user, wallet=1000, name='Tim',
                                       address='Romania')
            print('User has been created!')
