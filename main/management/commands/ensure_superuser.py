import os
import logging
from django.core.management.base import BaseCommand
from main.models import Users

class Command(BaseCommand):
    help = 'Creates an admin user if none exists'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')

        if not password:
            self.stdout.write(self.style.WARNING('DJANGO_ADMIN_PASSWORD environment variable not set. Using default password.'))
            password = 'admin123'  # More secure default password

        try:
            # Check if admin user exists
            if Users.objects.filter(is_admin=True).exists():
                self.stdout.write(self.style.SUCCESS('Admin user already exists'))
                return

            # Create admin user
            admin_user = Users(username=username, is_admin=True)
            # The password will be hashed in the save method of the Users model
            admin_user.password = password
            admin_user.save()
            
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to create admin user: {e}'))
            logging.error(f"Admin user creation failed: {e}")
            # Don't fail the deployment if user creation fails
            # This allows the app to start even if there's an issue with user creation
