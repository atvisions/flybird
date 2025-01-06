from django.urls import path
from .views import (
    DeleteAccountView, 
    ChangePasswordView,
    ChangePhoneView,
    BindEmailView,
    SendEmailCodeView,
    UnbindEmailView,
    ChangeEmailView,
    ChangeUsernameView
)

app_name = 'account'

urlpatterns = [
    path('delete/', DeleteAccountView.as_view(), name='delete'),
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    path('phone/', ChangePhoneView.as_view(), name='change-phone'),
    path('bind-email/', BindEmailView.as_view(), name='bind-email'),
    path('send-email-code/', SendEmailCodeView.as_view(), name='send-email-code'),
    path('unbind-email/', UnbindEmailView.as_view(), name='unbind-email'),
    path('change-email/', ChangeEmailView.as_view(), name='change-email'),
    path('username/', ChangeUsernameView.as_view(), name='change-username'),
]
