from django.contrib import admin
from .models import (
    MembershipTier, UserMembership, MembershipOrder,
    PointRule, UserPoint, PointRecord
)

@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'tier_type', 'price_monthly', 'price_quarterly', 
        'price_yearly', 'is_default', 'sort_order'
    ]
    list_editable = ['sort_order', 'is_default']
    search_fields = ['name']
    list_filter = ['tier_type', 'is_default']
    ordering = ['sort_order']

@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier', 'expire_time', 'is_expired', 'remaining_days']
    list_filter = ['tier', 'created_at']
    search_fields = ['user__phone', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = '是否过期'
    
    def remaining_days(self, obj):
        return obj.remaining_days
    remaining_days.short_description = '剩余天数'

@admin.register(MembershipOrder)
class MembershipOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_no', 'user', 'tier', 'amount',
        'payment_method', 'status', 'paid_time'
    ]
    list_filter = ['status', 'payment_method', 'tier']
    search_fields = ['order_no', 'user__username']
    raw_id_fields = ['user', 'tier']

@admin.register(PointRule)
class PointRuleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'event_type', 'points',
        'is_active', 'created_at'
    ]
    list_filter = ['is_active']
    search_fields = ['name', 'event_type']

@admin.register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'balance', 'total_earned',
        'total_spent', 'updated_at'
    ]
    search_fields = ['user__username']
    raw_id_fields = ['user']

@admin.register(PointRecord)
class PointRecordAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'event_type', 'points',
        'balance', 'created_at'
    ]
    list_filter = ['event_type']
    search_fields = ['user__username', 'description']
    raw_id_fields = ['user', 'rule'] 