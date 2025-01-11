from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MembershipTierViewSet, UserMembershipViewSet,
    MembershipOrderViewSet, PaymentCreateView,
    PaymentNotifyView, PaymentReturnView,
    AlipayNotifyView, AlipayReturnView,
    UserPointViewSet, PointRecordListView,
    PaymentVerifyView
)

router = DefaultRouter()
router.register(r'tiers', MembershipTierViewSet)
router.register(r'membership', UserMembershipViewSet, basename='membership')
router.register(r'orders', MembershipOrderViewSet, basename='orders')
router.register(r'points', UserPointViewSet, basename='points')

urlpatterns = [
    path('', include(router.urls)),
    path('payment/create/', PaymentCreateView.as_view(), name='create_payment'),
    path('payment/success/', PaymentReturnView.as_view(), name='payment_success'),
    path('payment/fail/', PaymentReturnView.as_view(), name='payment_fail'),
    path('payment/verify/', PaymentVerifyView.as_view(), name='payment_verify'),
    path('notify/alipay/', AlipayNotifyView.as_view(), name='alipay_notify'),
    path('return/alipay/', AlipayReturnView.as_view(), name='alipay_return'),
    path('points/records/', PointRecordListView.as_view(), name='point_records'),
]

