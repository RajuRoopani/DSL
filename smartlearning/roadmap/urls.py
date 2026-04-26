from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'skills', views.SkillViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'resources', views.ResourceViewSet)

urlpatterns = [
    path('generate/', views.generate_view, name='generate'),
    path('', views.generate_view, name='roadmap_list'),
    path('api/', include(router.urls)),
    path('api/generate/<int:skill_id>/', views.generate_roadmap_api, name='api-generate'),
]
