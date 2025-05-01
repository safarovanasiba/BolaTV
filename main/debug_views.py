from django.http import HttpResponse, JsonResponse
import os
import sys
import json
import django
from django.conf import settings

def health_check(request):
    """Simplified health check for production"""
    try:
        from django.db import connection
        connection.ensure_connection()
        return HttpResponse("OK", content_type="text/plain")
    except Exception as e:
        return HttpResponse(str(e), status=500, content_type="text/plain")
