from rest_framework import serializers
from users.models import User
from .basic import UserProfileSerializer, BasicInfoSerializer
from .work import WorkExperienceSerializer
from .education import EducationSerializer
from .skill import SkillSerializer
from .project import ProjectSerializer
from .certificate import CertificateSerializer
from .social import SocialLinkSerializer
from .layout import ProfileLayoutSerializer
from .portfolio import PortfolioSerializer
from .language import LanguageSerializer
from .intention import JobIntentionSerializer

class CompleteProfileSerializer(serializers.ModelSerializer):
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    social_links = SocialLinkSerializer(many=True, read_only=True)
    portfolios = PortfolioSerializer(many=True, read_only=True)
    profile_layout = ProfileLayoutSerializer(read_only=True)
    basic_info = BasicInfoSerializer(read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    job_intention = JobIntentionSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'phone',
            'nickname',
            'avatar',
            'email',
            'gender',
            'birthday',
            'location',
            'job_status',
            'work_years',
            'work_experiences',
            'educations',
            'skills',
            'projects',
            'certificates',
            'social_links',
            'portfolios',
            'profile_layout',
            'basic_info',
            'languages',
            'job_intention',
            'created_at'
        ]
        read_only_fields = ['phone', 'created_at'] 