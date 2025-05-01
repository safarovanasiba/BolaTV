from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    video_list, watch_video, dashboard, ariza_qoldirish, ariza_tashlandi,
    test_view, test_result, Home, login_view, register_view, logout_view
)
from .api_views import (
    ErtaklarViewSet, MultfilmlarViewSet, QoshiqlarViewSet, QiziqariMatematikaViewSet,
    IngliztiliViewSet, BadantarbiyaViewSet, RasmlarViewSet, ArizaViewSet,
    TestQuestionViewSet, TestResultViewSet, api_root
)
from .debug_views import health_check

# API router setup
router = DefaultRouter()
router.register('ertaklar', ErtaklarViewSet)
router.register('multfilmlar', MultfilmlarViewSet)
router.register('qoshiqlar', QoshiqlarViewSet)
router.register('matematika', QiziqariMatematikaViewSet)
router.register('ingliztili', IngliztiliViewSet)
router.register('badantarbiya', BadantarbiyaViewSet)
router.register('rasmlar', RasmlarViewSet)
router.register('ariza', ArizaViewSet)
router.register('test-questions', TestQuestionViewSet)
router.register('test-results', TestResultViewSet)

# Main URL patterns
urlpatterns = [
    # Health check endpoint - must be at the top for Railway
    path("health/", health_check, name="health_check"),
    path("healthz/", health_check, name="healthz"),  # Alternative path
    path("ready/", health_check, name="ready"),      # Kubernetes-style readiness
    path("live/", health_check, name="live"),        # Kubernetes-style liveness
    
    # Authentication endpoints
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    
    # Home page (landing page for non-authenticated users)
    path("", Home.as_view(), name="home"),
    
    # Web UI endpoints - these require authentication
    path("dashboard/", dashboard, name="dashboard"),
    path("ariza/", ariza_qoldirish, name="ariza_qoldirish"),
    path("ariza/tashlandi/", ariza_tashlandi, name="ariza_tashlandi"),
    path("test/", test_view, name="test"),
    path("test/result/", test_result, name="test_result"),
    path('video/<str:category>/<int:video_id>/', views.watch_video, name='watch_video'),
    
    # API endpoints
    path('api-root/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    
    # Swagger documentation - explicitly exclude these paths
    path('swagger/', dashboard, name='swagger'),
    
    # Video categories - using a catch-all pattern for compatibility with templates
    path("<str:category>/", video_list, name="video_list"),
]
