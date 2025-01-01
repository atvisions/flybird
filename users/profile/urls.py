from django.urls import path
from .views.basic import BasicProfileView, AvatarUploadView
from .views.work import WorkExperienceView, WorkExperienceDetailView
from .views.intention import JobIntentionView
from .views.layout import ProfileLayoutView
from .views.education import EducationView, EducationDetailView
from .views.project import ProjectView, ProjectDetailView
from .views.skill import SkillView, SkillDetailView
from .views.certificate import CertificateView, CertificateDetailView
from .views.language import LanguageView, LanguageDetailView
from .views.portfolio import PortfolioView, PortfolioDetailView
from .views.social import SocialLinkView, SocialLinkDetailView
from .views.completeness import ProfileCompletenessView
from .views.content_quality import ContentQualityView
from .views.profile import ProfileDataView
app_name = 'profile'

urlpatterns = [
    
    # 基本信息
    path('basic/', BasicProfileView.as_view(), name='basic'),
    path('avatar/upload/', AvatarUploadView.as_view(), name='avatar-upload'),
    
    # 完整度评分
    path('completeness/', ProfileCompletenessView.as_view(), name='completeness'),
    
    # 工作经历
    path('work-experiences/', WorkExperienceView.as_view(), name='work-experience-list'),
    path('work-experiences/<int:pk>/', WorkExperienceDetailView.as_view(), name='work-experience-detail'),
    
    # 求职意向
    path('job-intention/', JobIntentionView.as_view(), name='job-intention'),
    
    # 档案布局
    path('layout/', ProfileLayoutView.as_view(), name='layout'),
    
    # 教育经历
    path('educations/', EducationView.as_view(), name='education-list'),
    path('educations/<int:pk>/', EducationDetailView.as_view(), name='education-detail'),
    
    # 项目经历
    path('projects/', ProjectView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    
    # 技能特长
    path('skills/', SkillView.as_view(), name='skill-list'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    
    # 证书奖项
    path('certificates/', CertificateView.as_view(), name='certificate-list'),
    path('certificates/<int:pk>/', CertificateDetailView.as_view(), name='certificate-detail'),
    
    # 语言能力
    path('languages/', LanguageView.as_view(), name='language-list'),
    path('languages/<int:pk>/', LanguageDetailView.as_view(), name='language-detail'),
    
    # 作品集
    path('portfolios/', PortfolioView.as_view(), name='portfolio-list'),
    path('portfolios/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
    
    # 社交主页
    path('social-links/', SocialLinkView.as_view(), name='social-link-list'),
    path('social-links/<int:pk>/', SocialLinkDetailView.as_view(), name='social-link-detail'),
    
    # 内容质量
    path('content-quality/', ContentQualityView.as_view()),
    path('data/', ProfileDataView.as_view(), name='profile-data'),
    path('<str:module_type>/', ProfileDataView.as_view(), name='profile-module'),
    path('<str:module_type>/<int:pk>/', ProfileDataView.as_view(), name='profile-module-detail'),

]