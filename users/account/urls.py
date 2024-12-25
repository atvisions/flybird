from django.urls import path
from .views import (
    DeleteAccountView, 
    ChangePasswordView,
    ChangePhoneView
)

app_name = 'account'

urlpatterns = [
    path('delete/', DeleteAccountView.as_view(), name='delete'),
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    path('phone/', ChangePhoneView.as_view(), name='change-phone'),
]
