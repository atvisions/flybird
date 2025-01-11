from django.urls import path
from .views import (
    DeleteAccountView, 
    ChangePasswordView,
    ChangePhoneView,
    BindEmailView,
    SendEmailCodeView,
    UnbindEmailView,
    ChangeEmailView,
)

app_name = 'account'

urlpatterns = [
    # 账户管理
    path('delete/', DeleteAccountView.as_view(), name='delete'),
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    path('phone/', ChangePhoneView.as_view(), name='change-phone'),
    
    # 邮箱相关
    path('bind-email/', BindEmailView.as_view(), name='bind-email'),
    path('send-email-code/', SendEmailCodeView.as_view(), name='send-email-code'),
    path('unbind-email/', UnbindEmailView.as_view(), name='unbind-email'),
    path('change-email/', ChangeEmailView.as_view(), name='change-email'),
]
