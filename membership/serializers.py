from rest_framework import serializers
from .models import (
    MembershipTier, Privilege, TierPrivilege, UserMembership,
    MembershipOrder, PointRule, UserPoint, PointRecord
)

class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilege
        fields = ['id', 'name', 'key', 'description', 'value_type']

class TierPrivilegeSerializer(serializers.ModelSerializer):
    privilege = PrivilegeSerializer()
    
    class Meta:
        model = TierPrivilege
        fields = ['privilege', 'value']

class MembershipTierSerializer(serializers.ModelSerializer):
    privileges = TierPrivilegeSerializer(many=True, read_only=True)
    
    class Meta:
        model = MembershipTier
        fields = [
            'id', 'name', 'tier_type', 'price_monthly', 'price_quarterly',
            'price_yearly', 'description', 'privileges'
        ]

class UserMembershipSerializer(serializers.ModelSerializer):
    tier = MembershipTierSerializer()
    days_left = serializers.SerializerMethodField()
    
    class Meta:
        model = UserMembership
        fields = ['tier', 'expire_time', 'days_left', 'created_at']
        
    def get_days_left(self, obj):
        return obj.days_left if hasattr(obj, 'days_left') else 0

class MembershipOrderSerializer(serializers.ModelSerializer):
    tier = MembershipTierSerializer()
    
    class Meta:
        model = MembershipOrder
        fields = [
            'id', 'order_no', 'tier', 'amount', 'days',
            'payment_method', 'status', 'paid_time', 'created_at'
        ]

class PointRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointRule
        fields = ['id', 'name', 'event_type', 'points', 'description']

class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint
        fields = ['balance', 'total_earned', 'total_spent', 'updated_at']

class PointRecordSerializer(serializers.ModelSerializer):
    rule = PointRuleSerializer()
    
    class Meta:
        model = PointRecord
        fields = [
            'id', 'rule', 'points', 'balance', 'event_type',
            'description', 'created_at'
        ] 