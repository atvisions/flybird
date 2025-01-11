# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

from .profile.models import (
    BasicInfo, JobIntention, WorkExperience, Education,
    Project, Skill, Certificate, Language, Portfolio, SocialLink
)
from .models import User, VipOrder

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'username', 'vip_status_display', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_vip', 'vip_type', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('phone', 'username', 'uid')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('phone', 'username', 'password')}),
        (_('个人信息'), {
            'fields': ('avatar', 'background_image', 'position', 'bio'),
        }),
        (_('会员信息'), {
            'fields': ('is_vip', 'vip_type', 'vip_expire_time'),
        }),
        (_('权限'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('重要日期'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'password1', 'password2'),
        }),
    )

    # 添加会员管理的操作
    actions = ['set_as_monthly_vip', 'set_as_yearly_vip', 'set_as_lifetime_vip', 'remove_vip']
    
    def set_as_monthly_vip(self, request, queryset):
        """设置为月度会员"""
        from django.utils import timezone
        import datetime
        queryset.update(
            is_vip=True,
            vip_type='monthly',
            vip_expire_time=timezone.now() + datetime.timedelta(days=30)
        )
        self.message_user(request, f'成功将 {queryset.count()} 个用户设置为月度会员')
    set_as_monthly_vip.short_description = '设置为月度会员'

    def set_as_yearly_vip(self, request, queryset):
        """设置为年度会员"""
        from django.utils import timezone
        import datetime
        queryset.update(
            is_vip=True,
            vip_type='yearly',
            vip_expire_time=timezone.now() + datetime.timedelta(days=365)
        )
        self.message_user(request, f'成功将 {queryset.count()} 个用户设置为年度会员')
    set_as_yearly_vip.short_description = '设置为年度会员'

    def set_as_lifetime_vip(self, request, queryset):
        """设置为终身会员"""
        queryset.update(
            is_vip=True,
            vip_type='lifetime',
            vip_expire_time=None
        )
        self.message_user(request, f'成功将 {queryset.count()} 个用户设置为终身会员')
    set_as_lifetime_vip.short_description = '设置为终身会员'

    def remove_vip(self, request, queryset):
        """移除会员资格"""
        queryset.update(
            is_vip=False,
            vip_type='none',
            vip_expire_time=None
        )
        self.message_user(request, f'成功移除 {queryset.count()} 个用户的会员资格')
    remove_vip.short_description = '移除会员资格'

    def vip_status_display(self, obj):
        """显示会员状态"""
        if not obj.is_vip:
            return '普通用户'
        if obj.vip_type == 'lifetime':
            return '终身会员'
        if obj.vip_expire_time:
            from django.utils import timezone
            days_left = (obj.vip_expire_time - timezone.now()).days
            return f"{obj.get_vip_type_display()}（剩余{days_left}天）"
        return obj.get_vip_type_display()
    vip_status_display.short_description = '会员状态'

@admin.register(VipOrder)
class VipOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_no', 
        'user', 
        'vip_type', 
        'amount', 
        'status',
        'created_at', 
        'paid_at'
    )
    list_filter = ('status', 'vip_type', 'created_at')
    search_fields = ('order_no', 'user__phone', 'user__username')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    readonly_fields = ('order_no', 'created_at')
    
    fieldsets = (
        (None, {
            'fields': ('order_no', 'user', 'vip_type', 'amount')
        }),
        ('订单状态', {
            'fields': ('status', 'created_at', 'paid_at')
        }),
    )

    def has_delete_permission(self, request, obj=None):
        # 禁止删除已支付的订单
        if obj and obj.status == 'paid':
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        # 禁止修改已支付的订单的某些字段
        if obj and obj.status == 'paid':
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新建订单
            # 生成订单号
            import time
            import random
            timestamp = int(time.time())
            random_num = random.randint(1000, 9999)
            obj.order_no = f"VIP{timestamp}{random_num}"
        super().save_model(request, obj, form, change)

@admin.register(BasicInfo)
class BasicInfoAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'name', 
        'gender',
        'email',
        'created_at'
    ]
    list_filter = ['gender', 'created_at']
    search_fields = ['name', 'email', 'user__phone']
    raw_id_fields = ['user']

@admin.register(JobIntention)
class JobIntentionAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_type', 'expected_salary', 'expected_city', 'job_status')
    list_filter = ('job_type', 'job_status')
    search_fields = ('user__phone', 'expected_city')
    raw_id_fields = ('user',)

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('user__phone', 'company', 'position')
    raw_id_fields = ('user',)
    date_hierarchy = 'start_date'

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'major', 'degree', 'start_date', 'end_date')
    list_filter = ('degree', 'is_current')
    search_fields = ('user__phone', 'school', 'major')
    raw_id_fields = ('user',)
    date_hierarchy = 'start_date'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'role', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('user__phone', 'name', 'role')
    raw_id_fields = ('user',)
    date_hierarchy = 'start_date'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'level')
    list_filter = ('level',)
    search_fields = ('user__phone', 'name')
    raw_id_fields = ('user',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'type', 'issuing_authority', 'issue_date')
    list_filter = ('type',)
    search_fields = ('user__phone', 'name', 'issuing_authority')
    raw_id_fields = ('user',)
    date_hierarchy = 'issue_date'

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'proficiency', 'certification', 'quality_score')
    list_filter = ('proficiency',)
    search_fields = ('user__username', 'name', 'certification')
    raw_id_fields = ('user',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'url_link')
    search_fields = ('user__phone', 'title')
    raw_id_fields = ('user',)
    
    def url_link(self, obj):
        if obj.url:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url)
        return '-'
    url_link.short_description = '作品链接'

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'url_link')
    list_filter = ('platform',)
    search_fields = ('user__phone', 'platform')
    raw_id_fields = ('user',)
    
    def url_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url)
    url_link.short_description = '链接'