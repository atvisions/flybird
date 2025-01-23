from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    path('', views.ResumeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='resume-list'),
    path('<int:pk>/', views.ResumeViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='resume-detail'),
] 