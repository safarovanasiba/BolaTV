from django.http import HttpResponse, JsonResponse
import os
import sys
import json
import django
from django.conf import settings
from django.template import loader

def health_check(request):
    """Simplified health check for production"""
    try:
        # Check database connection
        from django.db import connection
        connection.ensure_connection()
        
        # Check template rendering capability
        try:
            loader.get_template('base.html')
            template_status = "OK"
        except Exception as e:
            template_status = f"ERROR: {str(e)}"
        
        # Create a simple response
        response_text = f"Database: OK\nTemplates: {template_status}"
        return HttpResponse(response_text, content_type="text/plain")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500, content_type="text/plain")
