"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Print debugging information
print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir("."))

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

try:
    application = get_wsgi_application()
    print("WSGI application initialized successfully")
except Exception as e:
    print(f"Error initializing WSGI application: {e}")
    # Return a minimal working application for debugging
    def minimal_application(environ, start_response):
        status = '200 OK'
        output = f'Error in WSGI application: {e}'.encode()
        response_headers = [('Content-type', 'text/plain'),
                           ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]
    application = minimal_application
