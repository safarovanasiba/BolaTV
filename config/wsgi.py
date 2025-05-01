"""
WSGI config for config project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Get the WSGI application
application = get_wsgi_application()

# This is used by gunicorn
app = application
