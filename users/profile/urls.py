from django.urls import path
from .views.basic import AvatarUploadView
from .views.layout import ProfileLayoutView
from .views.completeness import ProfileCompletenessView
from .views.content_quality import ContentQualityView
from .views.profile import ProfileDataView

app_name = 'profile'

urlpatterns = [
    # 头像上传（特殊处理）
    path('avatar/upload/', AvatarUploadView.as_view(), name='avatar-upload'),
    
    # 档案布局（特殊功能）
    path('layout/', ProfileLayoutView.as_view(), name='layout'),
    
    # 完整度评分（特殊功能）
    path('completeness/', ProfileCompletenessView.as_view(), name='completeness'),
    # 内容质量（特殊功能）
    path('content-quality/', ContentQualityView.as_view(), name='content-quality'),
    
    # 统一的档案数据管理接口
    path('data/', ProfileDataView.as_view(), name='profile-data'),
    path('<str:module_type>/', ProfileDataView.as_view(), name='profile-module'),
    path('<str:module_type>/<int:pk>/', ProfileDataView.as_view(), name='profile-module-detail'),
    
]