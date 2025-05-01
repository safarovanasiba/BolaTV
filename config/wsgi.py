"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
import logging
import traceback

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

from django.core.wsgi import get_wsgi_application

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    application = get_wsgi_application()
    logging.info("WSGI application initialized successfully")
except Exception as e:
    logging.error(f"Error initializing WSGI application: {e}")
    traceback.print_exc()
    
    # Return a minimal working application for debugging
    def minimal_application(environ, start_response):
        status = '500 Internal Server Error'
        error_msg = f'Error in WSGI application: {e}\n\n'
        error_msg += traceback.format_exc()
        output = error_msg.encode()
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(output))),
            ('X-Error-Source', 'WSGI Initialization')
        ]
        start_response(status, response_headers)
        return [output]
    
    application = minimal_application
