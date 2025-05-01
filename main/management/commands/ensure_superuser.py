import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
            
            if not password:
                self.stdout.write(self.style.WARNING('No superuser created. To create one, set the DJANGO_SUPERUSER_PASSWORD environment variable.'))
                return
                
            self.stdout.write(f'Creating superuser {username}')
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))
        else:
            self.stdout.write('Superuser already exists')
