from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tiers', views.MembershipTierViewSet)
router.register(r'membership', views.UserMembershipViewSet, basename='membership')
router.register(r'points', views.PointViewSet, basename='points')

app_name = 'membership'

urlpatterns = [
    path('', include(router.urls)),
    path('notify/alipay/', views.alipay_notify, name='alipay-notify'),
    path('notify/alipay/return/', views.alipay_return, name='alipay-return'),
    path('check-in/', views.check_in, name='check-in'),
] 