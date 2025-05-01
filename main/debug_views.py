from django.http import HttpResponse, JsonResponse
import os
import sys
import json
import django
from django.conf import settings

def health_check(request):
    """Robust health check endpoint for application monitoring"""
    try:
        # Check database connection
        from django.db import connection
        connection.ensure_connection()
        
        # Basic system info
        info = {
            'status': 'ok',
            'python_version': sys.version,
            'django_version': django.get_version(),
            'database': settings.DATABASES['default']['ENGINE'],
            'debug': settings.DEBUG,
            'request_path': request.path,
            'request_method': request.method,
            'remote_addr': request.META.get('REMOTE_ADDR', 'unknown'),
            'server_time': str(django.utils.timezone.now()),
        }
        
        # Return JSON for programmatic health checks
        if request.GET.get('format') == 'json':
            return JsonResponse(info)
        
        # Return human-readable text format
        response_text = "\nBolaTV Health Check\n"
        response_text += "==================\n\n"
        for key, value in info.items():
            response_text += f"{key}: {value}\n"
        
        return HttpResponse(response_text, content_type="text/plain")
        
    except Exception as e:
        error_response = {
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__
        }
        return JsonResponse(error_response, status=500)
