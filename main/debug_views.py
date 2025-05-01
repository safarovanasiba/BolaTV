from django.http import HttpResponse
import os
import sys

def health_check(request):
    """Simple view to check if the application is running"""
    python_version = sys.version
    env_vars = '\n'.join([f"{k}={v}" for k, v in os.environ.items() if not k.startswith('_')])
    
    response = f"""
    BolaTV Health Check
    ------------------
    Python Version: {python_version}
    Environment Variables:
    {env_vars}
    """
    
    return HttpResponse(response, content_type="text/plain")
