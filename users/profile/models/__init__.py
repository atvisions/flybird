"""
用户档案模型模块
"""

from .basic import BasicInfo
from .intention import JobIntention
from .work import WorkExperience
from .education import Education
from .skill import Skill
from .language import Language
from .certificate import Certificate
from .portfolio import Portfolio
from .project import Project
from .social import SocialLink
from .layout import ProfileLayout
from .ai import AIOptimizationSuggestion, AIQualityImprovement, AIOptimizationQuota

__all__ = [
    'BasicInfo',
    'JobIntention',
    'WorkExperience',
    'Education',
    'Skill',
    'Language',
    'Certificate',
    'Portfolio',
    'Project',
    'SocialLink',
    'AIOptimizationSuggestion',
    'AIQualityImprovement',
    'AIOptimizationQuota',
    'ProfileLayout',
]
