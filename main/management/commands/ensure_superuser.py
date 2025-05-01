import os
from django.core.management.base import BaseCommand
from main.models import Users
import logging

Users = Users

class Command(BaseCommand):
    help = 'Creates an admin user if none exists'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not password:
            self.stdout.write(self.style.WARNING('DJANGO_SUPERUSER_PASSWORD environment variable not set. Using default password.'))
            password = 'admin'

        if Users.objects.filter(is_admin=True).exists():
            self.stdout.write(self.style.SUCCESS('Admin user already exists'))
            return

        try:
            Users.objects.create(username=username, password=password, is_admin=True)
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to create admin user: {e}'))
            logging.error(f"Admin user creation failed: {e}")
