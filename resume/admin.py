from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'status', 'is_public', 'view_count', 'download_count', 'created_at']
    list_filter = ['status', 'is_public']
    search_fields = ['name', 'description', 'creator__username']
    readonly_fields = ['view_count', 'download_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
