"""
用户档案模型模块
"""

from .basic import BasicInfo
from .intention import JobIntention
from .layout import ProfileLayout
from .work import WorkExperience
from .education import Education
from .skill import Skill
from .project import Project
from .certificate import Certificate
from .language import Language
from .portfolio import Portfolio
from .social import SocialLink
from .study import Study

__all__ = [
    'BasicInfo',
    'JobIntention',
    'ProfileLayout',
    'WorkExperience',
    'Education',
    'Skill',
    'Project',
    'Certificate',
    'Language',
    'Portfolio',
    'SocialLink',
    'Study'
]
