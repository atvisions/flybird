from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tiers', views.MembershipTierViewSet)
router.register(r'membership', views.UserMembershipViewSet, basename='membership')
router.register(r'points', views.PointViewSet, basename='points')

app_name = 'membership'

# API路由
api_urlpatterns = [
    path('', include(router.urls)),
    path('purchase/', views.MembershipPurchaseView.as_view(), name='purchase'),
    path('notify/alipay/', views.alipay_notify, name='alipay-notify'),
    path('notify/alipay/return/', views.alipay_return, name='alipay-return'),
    path('check-in/', views.check_in, name='check-in'),
]

# 支付结果页面路由
payment_urlpatterns = [
    path('success/', views.payment_success, name='payment-success'),
    path('fail/', views.payment_fail, name='payment-fail'),
]

# 导出不同的路由组
urlpatterns = api_urlpatterns 
