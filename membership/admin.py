from django.contrib import admin
from .models import (
    MembershipTier, UserMembership, MembershipOrder,
    UserPoint, PointRecord, PointRule
)

@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sort_order', 'price_monthly', 'price_quarterly', 
        'price_yearly', 'status', 'is_default', 'created_at'
    ]
    list_editable = ['sort_order', 'price_monthly', 'price_quarterly', 'price_yearly', 'status']
    list_filter = ['status', 'is_default']
    search_fields = ['name', 'description']
    ordering = ['sort_order']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'sort_order', 'status', 'is_default')
        }),
        ('价格设置', {
            'fields': ('price_monthly', 'price_quarterly', 'price_yearly')
        }),
        ('权益配置', {
            'fields': ('benefits',)
        })
    )

@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'tier',
        'expire_time',
        'membership_status',
        'created_at'
    ]
    list_filter = [
        'tier',
        'expire_time',
    ]
    search_fields = ['user__username', 'user__phone']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    
    def membership_status(self, obj):
        """会员状态"""
        if not obj.tier:
            return '未开通'
        if obj.is_active:
            return f'有效({obj.remaining_days}天)'
        return '已过期'
    membership_status.short_description = '会员状态'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'tier')

@admin.register(MembershipOrder)
class MembershipOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_no', 'user', 'tier', 'amount', 'days',
        'payment_method', 'status', 'created_at', 'paid_time'
    ]
    list_filter = ['status', 'payment_method', 'tier']
    search_fields = ['order_no', 'user__username', 'user__phone']
    raw_id_fields = ['user', 'tier']
    date_hierarchy = 'created_at'
    readonly_fields = ['order_no', 'created_at', 'paid_time']

@admin.register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'balance', 'total_earned', 'point_level',
        'created_at', 'updated_at'
    ]
    list_filter = ['point_level']
    search_fields = ['user__username', 'user__phone']
    raw_id_fields = ['user']
    readonly_fields = ['total_earned', 'created_at', 'updated_at']

@admin.register(PointRecord)
class PointRecordAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'points', 'balance', 'event_type',
        'description', 'created_at'
    ]
    list_filter = ['event_type']
    search_fields = ['user__username', 'user__phone', 'description']
    raw_id_fields = ['user', 'rule']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

@admin.register(PointRule)
class PointRuleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'event_type', 'points', 'is_active',
        'created_at', 'updated_at'
    ]
    list_editable = ['points', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'event_type', 'description']
    ordering = ['event_type']
    readonly_fields = ['created_at', 'updated_at'] 