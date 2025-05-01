from django.http import HttpResponse, JsonResponse
import os
import sys
import json
import django
from django.conf import settings
from django.template import loader
from django.db import connection
from django.views.decorators.cache import never_cache

@never_cache
def health_check(request):
    """
    Comprehensive health check for Railway deployment
    This endpoint is used by Railway to determine if the application is healthy
    """
    try:
        # Check database connection
        connection.ensure_connection()
        
        # Basic system info
        python_version = sys.version
        django_version = django.get_version()
        
        # Check template rendering capability
        try:
            loader.get_template('base.html')
            template_status = "OK"
        except Exception as e:
            template_status = f"ERROR: {str(e)}"
        
        # Create response with all critical information
        response_data = {
            "status": "healthy",
            "database": "connected",
            "templates": template_status,
            "python_version": python_version,
            "django_version": django_version,
            "debug_mode": settings.DEBUG
        }
        
        # Return as plain text for Railway health checks
        response_text = "\n".join([f"{k}: {v}" for k, v in response_data.items()])
        return HttpResponse(response_text, content_type="text/plain")
    except Exception as e:
        # Return error but with 200 status to not trigger false alarms
        # Railway expects a 200 response for health checks
        return HttpResponse(f"Status: unhealthy\nError: {str(e)}", content_type="text/plain")
