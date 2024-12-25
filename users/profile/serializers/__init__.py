"""
用户档案序列化器模块
"""

from .basic import BasicInfoSerializer
from .intention import JobIntentionSerializer
from .layout import ProfileLayoutSerializer
from .work import WorkExperienceSerializer
from .education import EducationSerializer
from .skill import SkillSerializer
from .project import ProjectSerializer
from .certificate import CertificateSerializer
from .language import LanguageSerializer
from .portfolio import PortfolioSerializer
from .social import SocialLinkSerializer

__all__ = [
    'BasicInfoSerializer',
    'JobIntentionSerializer',
    'ProfileLayoutSerializer',
    'WorkExperienceSerializer',
    'EducationSerializer',
    'SkillSerializer',
    'ProjectSerializer',
    'CertificateSerializer',
    'LanguageSerializer',
    'PortfolioSerializer',
    'SocialLinkSerializer'
]
