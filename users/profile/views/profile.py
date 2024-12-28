import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import (
    BasicInfo, JobIntention, WorkExperience, Education,
    Project, Skill, Certificate, Language, Portfolio, SocialLink
)
from ..serializers import (
    BasicInfoSerializer, JobIntentionSerializer, WorkExperienceSerializer,
    EducationSerializer, ProjectSerializer, SkillSerializer,
    CertificateSerializer, LanguageSerializer, PortfolioSerializer,
    SocialLinkSerializer
)

logger = logging.getLogger('users')

class CompleteProfileView(APIView):
    """完整档案视图"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            logger.info(f"获取用户 {user.phone} 的完整档案")
            
            # 获取各部分数据
            basic_info = BasicInfo.objects.get(user=user)
            job_intention = JobIntention.objects.filter(user=user).first()
            work_experiences = WorkExperience.objects.filter(user=user)
            educations = Education.objects.filter(user=user)
            projects = Project.objects.filter(user=user)
            skills = Skill.objects.filter(user=user)
            certificates = Certificate.objects.filter(user=user)
            languages = Language.objects.filter(user=user)
            portfolios = Portfolio.objects.filter(user=user)
            social_links = SocialLink.objects.filter(user=user)
            
            # 记录数据量
            logger.info(f"工作经历: {work_experiences.count()} 条")
            logger.info(f"教育经历: {educations.count()} 条")
            logger.info(f"技能特长: {skills.count()} 条")
            logger.info(f"证书资质: {certificates.count()} 条")
            logger.info(f"语言能力: {languages.count()} 条")
            logger.info(f"作品集: {portfolios.count()} 条")
            logger.info(f"社交链接: {social_links.count()} 条")
            
            # 序列化数据
            data = {
                'basic_info': BasicInfoSerializer(basic_info).data,
                'job_intention': JobIntentionSerializer(job_intention).data if job_intention else None,
                'work_experiences': WorkExperienceSerializer(work_experiences, many=True).data,
                'educations': EducationSerializer(educations, many=True).data,
                'projects': ProjectSerializer(projects, many=True).data,
                'skills': SkillSerializer(skills, many=True).data,
                'certificates': CertificateSerializer(certificates, many=True).data,
                'languages': LanguageSerializer(languages, many=True).data,
                'portfolios': PortfolioSerializer(portfolios, many=True).data,
                'social_links': SocialLinkSerializer(social_links, many=True).data,
            }
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': data
            })
            
        except BasicInfo.DoesNotExist:
            logger.error(f"用户 {user.id} 基本信息不存在")
            return Response({
                'code': 404,
                'message': '基本信息不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"获取完整档案失败: {str(e)}")
            logger.error(f"错误详情: {e.__class__.__name__}")
            return Response({
                'code': 500,
                'message': '获取完整档案失败',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 