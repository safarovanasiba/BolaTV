from django.http import HttpResponse

def health_check(request):
    """Simple view to check if the application is running"""
    return HttpResponse("BolaTV is running!", content_type="text/plain")
