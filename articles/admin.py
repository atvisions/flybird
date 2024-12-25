from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = '文章数'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover_display', 'category', 'author', 'status', 'views', 'likes', 'is_featured', 'created_at')
    list_filter = ('status', 'category', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def cover_display(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.cover.url
            )
        return '-'
    cover_display.short_description = '封面'

    fieldsets = (
        ('基本信息', {
            'fields': (('title', 'slug'), 'author', 'category', 'cover', 'summary')
        }),
        ('内容', {
            'fields': ('content',)
        }),
        ('设置', {
            'fields': ('status', 'is_featured', 'published_at'),
            'classes': ('collapse',)
        }),
        ('统计', {
            'fields': ('views', 'likes'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新建文章
            obj.author = request.user  # 设置作者为当前用户
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # 编辑时
            return ('views', 'likes')
        return ()  # 新建时没有只读字段

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'article', 'author', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('content', 'author__username', 'article__title')
    raw_id_fields = ('article', 'author', 'parent')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '内容预览' 