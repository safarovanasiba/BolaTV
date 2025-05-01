from django.urls import path, include, re_path
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
    # Health check endpoints - must be at the top for fast response
    path("health/", health_check, name="health_check"),
    path("healthz/", health_check, name="healthz"),
    path("ready/", health_check, name="ready"),
    path("live/", health_check, name="live"),
    
    # Critical user flows
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", Home.as_view(), name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    
    # Secondary flows - can be loaded after initial rendering
    path("register/", register_view, name="register"),
    path("ariza/", ariza_qoldirish, name="ariza_qoldirish"),
    path("ariza/tashlandi/", ariza_tashlandi, name="ariza_tashlandi"),
    path("test/", test_view, name="test"),
    path("test/result/", test_result, name="test_result"),
    path('video/<str:category>/<int:video_id>/', views.watch_video, name='watch_video'),
    
    # API endpoints
    path('api-root/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    
    # Remove the problematic Swagger redirection
    # path('swagger/', dashboard, name='swagger'),
    
    # IMPORTANT: Exclude Swagger from catch-all pattern
    # Explicitly exclude paths that should be handled by the root URLconf
    re_path(r'^(?!swagger|api-docs|redoc)(?P<category>[\w-]+)/$', video_list, name="video_list"),

    # Health check endpoint
    path("health-check/", health_check, name="app_health_check"),
    path("text/", views.simple_text_response, name="simple_text_response"),
]
