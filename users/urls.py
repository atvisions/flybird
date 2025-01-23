from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', include('users.auth.urls')),          # 认证相关路由
    path('account/', include('users.account.urls')),    # 账户相关路由
    path('profile/', include('users.profile.urls')),    # 档案相关路由
    path('api-urls/', views.list_urls, name='list-urls'),
    path('userInfo/', views.UserInfoView.as_view(), name='user-info'),
    path('userInfo/avatar/', views.AvatarUploadView.as_view(), name='avatar'),
    path('userInfo/background/', views.BackgroundUploadView.as_view(), name='background'),
    path('users/<int:user_id>/', views.UserPublicInfoView.as_view(), name='user-public-info'),
]