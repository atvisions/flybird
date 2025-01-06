from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', include('users.auth.urls')),         # 认证相关路由
    path('account/', include('users.account.urls')),    # 账户相关路由
    path('profile/', include('users.profile.urls')),    # 档案相关路由
    path('api-urls/', views.list_urls, name='list-urls'),
]
