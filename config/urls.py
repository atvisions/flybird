from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from membership.urls import api_urlpatterns as membership_api_urls
from membership.urls import payment_urlpatterns as membership_payment_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/articles/', include('articles.urls')),
    path('api/v1/qa/', include('qa.urls')),
    path('api/v1/membership/', include(membership_api_urls)),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('api/v1/users/', include('users.urls')),
    # 支付结果页面路由
    path('payment/', include(membership_payment_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)