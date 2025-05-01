import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import logging

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not password:
            self.stdout.write(self.style.WARNING('DJANGO_SUPERUSER_PASSWORD environment variable not set. Using default password.'))
            password = 'admin'

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            return

        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to create superuser: {e}'))
            logging.error(f"Superuser creation failed: {e}")
