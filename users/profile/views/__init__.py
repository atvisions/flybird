"""
用户档案视图模块
"""

from .basic import BasicProfileView, AvatarUploadView
from .work import WorkExperienceView, WorkExperienceDetailView
from .education import EducationView, EducationDetailView
from .skill import SkillView, SkillDetailView
from .project import ProjectView, ProjectDetailView
from .certificate import CertificateView, CertificateDetailView
from .social import SocialLinkView, SocialLinkDetailView
from .layout import ProfileLayoutView
from .portfolio import PortfolioView, PortfolioDetailView
from .import_view import ResumeImportView

__all__ = [
    'BasicProfileView',
    'AvatarUploadView',
    'WorkExperienceView',
    'WorkExperienceDetailView',
    'EducationView',
    'EducationDetailView',
    'SkillView',
    'SkillDetailView',
    'ProjectView',
    'ProjectDetailView',
    'CertificateView',
    'CertificateDetailView',
    'SocialLinkView',
    'SocialLinkDetailView',
    'ProfileLayoutView',
    'PortfolioView',
    'PortfolioDetailView',
    'ResumeImportView'
] 