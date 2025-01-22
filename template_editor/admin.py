# template_editor/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Template

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'sort_order', 'created_at')
    list_editable = ('sort_order',)
    search_fields = ('name',)
    ordering = ('sort_order',)
    list_per_page = 20

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_thumbnail', 'category', 'creator', 
                   'status', 'is_public', 'page_count', 'created_at')
    list_filter = ('category', 'status', 'is_public', 'created_at')
    search_fields = ('name', 'description', 'keywords')
    ordering = ('-created_at',)
    list_per_page = 20
    readonly_fields = ('creator', 'created_at', 'updated_at', 'page_count')
    
    def show_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" />', obj.thumbnail.url)
        return "无缩略图"
    show_thumbnail.short_description = '缩略图'

    def page_count(self, obj):
        return obj.get_page_count()
    page_count.short_description = '页面数量'

    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新建而不是修改
            obj.creator = request.user
            super().save_model(request, obj, form, change)
            # 创建第一个页面
            obj.add_page()
        else:
            super().save_model(request, obj, form, change)

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'thumbnail', 'category', 'keywords')
        }),
        ('状态设置', {
            'fields': ('status', 'is_public')
        }),
        ('画布数据', {
            'fields': ('pages',),
            'classes': ('collapse',)
        }),
        ('其他信息', {
            'fields': ('creator', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )