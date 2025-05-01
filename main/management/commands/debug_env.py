import os
import sys
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Prints debugging information about the environment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Python version: %s' % sys.version))
        self.stdout.write(self.style.SUCCESS('Current directory: %s' % os.getcwd()))
        
        try:
            files = os.listdir('.')
            self.stdout.write(self.style.SUCCESS('Files in current directory: %s' % ', '.join(files)))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Error listing directory: %s' % e))
        
        try:
            import django
            self.stdout.write(self.style.SUCCESS('Django version: %s' % django.__version__))
        except ImportError:
            self.stdout.write(self.style.ERROR('Django not installed'))
        
        # Print environment variables
        self.stdout.write(self.style.SUCCESS('Environment variables:'))
        for key, value in os.environ.items():
            if not key.startswith('_'):  # Skip internal variables
                self.stdout.write(f'  {key}={value}')
