# template_editor/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'template_editor'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'templates', views.TemplateViewSet, basename='template')

urlpatterns = [
    path('', include(router.urls)),
]