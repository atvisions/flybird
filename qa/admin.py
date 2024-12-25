from django.contrib import admin
from django.utils.html import format_html
from .models import Question, Answer, Comment

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'answer_count', 'views', 'likes', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'tags')
    raw_id_fields = ('author', 'accepted_answer')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def answer_count(self, obj):
        return obj.answers.count()
    answer_count.short_description = '回答数'

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'content', 'author', 'tags')
        }),
        ('状态', {
            'fields': ('status', 'accepted_answer'),
            'classes': ('collapse',)
        }),
        ('统计', {
            'fields': ('views', 'likes'),
            'classes': ('collapse',)
        }),
    )

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    raw_id_fields = ('author',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'author', 'likes', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('content', 'author__username', 'question__title')
    raw_id_fields = ('question', 'author')
    inlines = [CommentInline]

    def question_title(self, obj):
        return obj.question.title
    question_title.short_description = '问题'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'target', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username')
    raw_id_fields = ('question', 'answer', 'author')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '内容'

    def target(self, obj):
        if obj.question:
            return f'问题: {obj.question.title}'
        return f'答案: {obj.answer.question.title}'
    target.short_description = '评论对象' 