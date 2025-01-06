from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    PasswordLoginView, 
    RegisterView, 
    LogoutView,
    SendSmsCodeView,
    ResetPasswordView,
    ChangePhoneView,
)

app_name = 'auth'

urlpatterns = [
    # 登录注册相关
    path('login/password/', PasswordLoginView.as_view(), name='login-password'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Token相关
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # 短信验证码
    path('sms/send/', SendSmsCodeView.as_view(), name='sms-send'),
    
    # 重置密码
    path('password/reset/', ResetPasswordView.as_view(), name='password-reset'),
    
    # 更换手机号
    path('change-phone/', ChangePhoneView.as_view(), name='change-phone'),
]
