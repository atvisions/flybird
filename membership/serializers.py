from rest_framework import serializers
from .models import (
    MembershipTier, UserMembership, MembershipOrder, 
    UserPoint, PointRecord, PointRule
)
from django.utils import timezone

class MembershipTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipTier
        fields = [
            'id', 'name', 'description', 'sort_order',
            'price_monthly', 'price_quarterly', 'price_yearly',
            'benefits'
        ]

class UserMembershipSerializer(serializers.ModelSerializer):
    tier = MembershipTierSerializer()
    days_left = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = UserMembership
        fields = [
            'tier', 'expire_time', 'status', 
            'days_left', 'is_active', 'created_at'
        ]
        
    def get_days_left(self, obj):
        if not obj.expire_time or not obj.status:
            return 0
        if obj.expire_time < timezone.now():
            return 0
        return (obj.expire_time - timezone.now()).days
        
    def get_is_active(self, obj):
        return obj.is_active

class MembershipOrderSerializer(serializers.ModelSerializer):
    tier = MembershipTierSerializer()
    
    class Meta:
        model = MembershipOrder
        fields = [
            'order_no', 'tier', 'amount', 'days',
            'payment_method', 'status', 'paid_time',
            'created_at'
        ]

class PointRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointRule
        fields = ['name', 'event_type', 'points', 'description']

class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint
        fields = ['balance', 'total_earned', 'point_level']

class PointRecordSerializer(serializers.ModelSerializer):
    rule = PointRuleSerializer()
    
    class Meta:
        model = PointRecord
        fields = [
            'points', 'balance', 'event_type',
            'description', 'created_at'
        ] 