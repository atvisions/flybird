from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .profile.models import (
    BasicInfo,
    JobIntention,
    WorkExperience,
    Education,
    Skill,
    Project,
    Certificate,
    Language,
    Portfolio,
    SocialLink,
    ProfileLayout
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'username', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('phone', 'username')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('phone', 'username', 'password')}),
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

@admin.register(BasicInfo)
class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender', 'birthday', 'created_at')
    search_fields = ('user__phone', 'name')
    list_filter = ('gender', 'created_at')

@admin.register(JobIntention)
class JobIntentionAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_type', 'expected_salary', 'created_at')
    search_fields = ('user__phone',)
    list_filter = ('job_type', 'created_at')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'start_date', 'end_date', 'is_current')
    search_fields = ('user__phone', 'company', 'position')
    list_filter = ('is_current', 'start_date')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'major', 'degree', 'start_date', 'end_date', 'is_current')
    search_fields = ('user__phone', 'school', 'major')
    list_filter = ('degree', 'is_current')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'level', 'created_at')
    search_fields = ('user__phone', 'name')
    list_filter = ('level', 'created_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'role', 'start_date', 'end_date', 'is_current')
    search_fields = ('user__phone', 'name', 'role')
    list_filter = ('is_current', 'start_date')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'issuing_authority', 'issue_date')
    search_fields = ('user__phone', 'name', 'issuing_authority')
    list_filter = ('issue_date',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'level', 'created_at')
    search_fields = ('user__phone', 'name')
    list_filter = ('level', 'created_at')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    search_fields = ('user__phone', 'title')
    list_filter = ('created_at',)

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'url', 'created_at')
    search_fields = ('user__phone', 'platform')
    list_filter = ('platform', 'created_at')

@admin.register(ProfileLayout)
class ProfileLayoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__phone',)
    list_filter = ('created_at',) 