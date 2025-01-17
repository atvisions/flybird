from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'template-categories', views.TemplateCategoryViewSet)
router.register(r'templates', views.ResumeTemplateViewSet, basename='template')
router.register(r'resumes', views.ResumeViewSet, basename='resume')
router.register(r'component-categories', views.ComponentCategoryViewSet)
router.register(r'components', views.ComponentViewSet)

app_name = 'resume'

urlpatterns = [
    path('', include(router.urls)),
] 