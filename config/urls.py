from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/articles/', include('articles.urls')),
    path('api/v1/qa/', include('qa.urls')),
    path('api/v1/membership/', include('membership.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/template-editor/', include('template_editor.urls')),  # 确保这行存在
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)