from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser'

    CREDENTIALS = os.environ.get("SUPERUSER_CREDENTIALS").split(",")

    print(CREDENTIALS)

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('username', self.CREDENTIALS[0], self.CREDENTIALS[1])
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))