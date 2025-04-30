from django.urls import path

from . import views
from .views import UsersViews, video_list, watch_video, dashboard, user_logout, ariza_qoldirish, ariza_tashlandi, \
    test_view, test_result, Home

urlpatterns = [
    path("",Home.as_view(), name="home"),
    path("login/", UsersViews, name="user"),
    path("logout/", user_logout, name="logout"),
    path("ariza/", ariza_qoldirish, name="ariza_qoldirish"),
    path("ariza/tashlandi/", ariza_tashlandi, name="ariza_tashlandi"),
    path("test/", test_view, name="test"),
    path("test/result/", test_result, name="test_result"),
    path("dashboard/", dashboard, name="dashboard"),

    # Video ro‘yxatlari
    path("<str:category>/", video_list, name="video_list"),

    # Videolarni ko‘rish
    path('video/<str:category>/<int:video_id>/', views.watch_video, name='watch_video')

]
