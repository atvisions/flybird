"""
用户档案模型模块
"""

from .basic import BasicInfo
from .intention import JobIntention
from .work import WorkExperience
from .education import Education
from .project import Project
from .skill import Skill
from .certificate import Certificate
from .language import Language
from .portfolio import Portfolio
from .social import SocialLink
from .layout import ProfileLayout
from .score import ProfileScore

__all__ = [
    'BasicInfo',
    'JobIntention',
    'WorkExperience',
    'Education',
    'Project',
    'Skill',
    'Certificate',
    'Language',
    'Portfolio',
    'SocialLink',
    'ProfileLayout',
    'ProfileScore'
]
