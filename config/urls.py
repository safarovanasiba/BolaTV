"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from main.debug_views import health_check

# Add DRF and Swagger UI
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def simple_health(request):
    """A very basic health check that will always succeed"""
    return HttpResponse("OK", content_type="text/plain")

# Create the schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="BolaTV API",
        default_version='v1',
        description="API documentation for BolaTV",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Define URL patterns - ORDER MATTERS!
urlpatterns = [
    # Health check endpoints for quick response
    path("health/", health_check, name="health_check"),
    path("ping/", simple_health, name="simple_health"),
    
    # Admin site
    path("admin/", admin.site.urls),
    
    # Swagger UI endpoints - MUST be before main app URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Main app URLs - MUST be last to avoid capturing Swagger URLs
    path("", include('main.urls')),
]
