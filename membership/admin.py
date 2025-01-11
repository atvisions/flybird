from django.contrib import admin
from .models import UserMembership
from django.utils import timezone
import datetime

@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_type', 'expire_time', 'membership_status', 'created_at')
    list_filter = ('membership_type', 'created_at')
    search_fields = ('user__username', 'user__phone', 'user__email')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    
    actions = ['set_monthly_membership', 'set_yearly_membership', 'set_lifetime_membership', 'remove_membership']

    def membership_status(self, obj):
        if obj.membership_type == 'none':
            return '普通用户'
        if obj.membership_type == 'lifetime':
            return '终身会员'
        if obj.expire_time:
            days_left = (obj.expire_time - timezone.now()).days
            if days_left > 0:
                return f"{obj.get_membership_type_display()}（剩余{days_left}天）"
            return '已过期'
        return obj.get_membership_type_display()
    membership_status.short_description = '会员状态'

    def set_monthly_membership(self, request, queryset):
        queryset.update(
            membership_type='monthly',
            expire_time=timezone.now() + datetime.timedelta(days=30)
        )
        self.message_user(request, f'已将 {queryset.count()} 个用户设置为月度会员')
    set_monthly_membership.short_description = '设置为月度会员'

    def set_yearly_membership(self, request, queryset):
        queryset.update(
            membership_type='yearly',
            expire_time=timezone.now() + datetime.timedelta(days=365)
        )
        self.message_user(request, f'已将 {queryset.count()} 个用户设置为年度会员')
    set_yearly_membership.short_description = '设置为年度会员'

    def set_lifetime_membership(self, request, queryset):
        queryset.update(
            membership_type='lifetime',
            expire_time=None
        )
        self.message_user(request, f'已将 {queryset.count()} 个用户设置为终身会员')
    set_lifetime_membership.short_description = '设置为终身会员'

    def remove_membership(self, request, queryset):
        queryset.update(
            membership_type='none',
            expire_time=None
        )
        self.message_user(request, f'已移除 {queryset.count()} 个用户的会员资格')
    remove_membership.short_description = '移除会员资格'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 同步更新用户表中的会员状态
        user = obj.user
        user.is_vip = obj.membership_type != 'none'
        user.vip_type = obj.membership_type
        user.vip_expire_time = obj.expire_time
        user.save(update_fields=['is_vip', 'vip_type', 'vip_expire_time']) 