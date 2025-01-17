from django.contrib import admin
from .models import TemplateCategory, ResumeTemplate, Resume, Component, ComponentCategory

@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    ordering = ['sort_order', 'id']

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_system', 'creator', 'created_at']
    list_filter = ['type', 'is_system']
    search_fields = ['name', 'description']
    readonly_fields = ['creator']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # 如果是新创建的对象
            obj.creator = request.user
        super().save_model(request, obj, form, change)

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'category', 'creator', 'status',
        'is_vip', 'created_at'
    ]
    list_filter = ['status', 'is_vip', 'category']
    search_fields = ['name', 'description']
    readonly_fields = ['creator']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # 如果是新创建的对象
            obj.creator = request.user
        super().save_model(request, obj, form, change)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'template', 'is_public', 'created_at']
    list_filter = ['is_public', 'template']
    search_fields = ['name', 'user__username']
    readonly_fields = ['user']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # 如果是新创建的对象
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(ComponentCategory)
class ComponentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'icon', 'sort_order', 'is_active']
    list_editable = ['sort_order', 'is_active']
    search_fields = ['name', 'code', 'description']
    list_filter = ['is_active']
    ordering = ['sort_order', 'id'] 