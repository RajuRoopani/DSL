from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'progress', views.ProgressViewSet)

urlpatterns = [
    path('', views.dummy_view, name='progress'),
    path('api/', include(router.urls)),
    path('api/leaderboard/', views.leaderboard, name='leaderboard'),
]
