# users/profile/views/profile.py
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Prefetch
# 修改 User 的导入路径
from users.models import User  # 从主 users app 导入 User 模型
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

# users/profile/views/profile.py
class ProfileDataView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取完整档案数据"""
        try:
            user = request.user
            logger.info(f"获取用户 {user.id} 的档案数据")
            
            try:
                user = User.objects.prefetch_related(
                    Prefetch('basic_info', queryset=BasicInfo.objects.filter(user=user)),
                    Prefetch('job_intention', queryset=JobIntention.objects.filter(user=user)),
                    Prefetch('work_experiences', queryset=WorkExperience.objects.filter(user=user).order_by('-start_date')),
                    Prefetch('educations', queryset=Education.objects.filter(user=user).order_by('-start_date')),
                    Prefetch('projects', queryset=Project.objects.filter(user=user).order_by('-start_date')),
                    Prefetch('skills', queryset=Skill.objects.filter(user=user).order_by('order')),  # 改为 skills
                    Prefetch('certificates', queryset=Certificate.objects.filter(user=user).order_by('-issue_date')),
                    Prefetch('languages', queryset=Language.objects.filter(user=user).order_by('id')),
                    Prefetch('portfolios', queryset=Portfolio.objects.filter(user=user).order_by('order')),
                    Prefetch('social_links', queryset=SocialLink.objects.filter(user=user).order_by('id'))
                ).get(id=user.id)
                
                # 序列化数据
                data = {
                    'basic_info': BasicInfoSerializer(user.basic_info).data if hasattr(user, 'basic_info') else None,
                    'job_intention': JobIntentionSerializer(user.job_intention).data if hasattr(user, 'job_intention') else None,
                    'work_experience': WorkExperienceSerializer(user.work_experiences.all(), many=True).data,
                    'education': EducationSerializer(user.educations.all(), many=True).data,
                    'project': ProjectSerializer(user.projects.all(), many=True).data,
                    'skill': SkillSerializer(user.skills.all(), many=True).data,  # 改为 skills
                    'certificate': CertificateSerializer(user.certificates.all(), many=True).data,
                    'language': LanguageSerializer(user.languages.all(), many=True).data,
                    'portfolio': PortfolioSerializer(user.portfolios.all(), many=True).data,
                    'social_link': SocialLinkSerializer(user.social_links.all(), many=True).data
                }
                
                # 记录数据统计
                stats = {key: len(value) for key, value in data.items() if isinstance(value, list)}
                logger.info(f"用户 {user.id} 档案数据统计: {stats}")
                
                return Response({
                    'code': 200,
                    'message': '获取成功',
                    'data': data
                })
                
            except User.DoesNotExist:
                logger.error(f"用户 {request.user.id} 不存在")
                return Response({
                    'code': 404,
                    'message': '用户不存在',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"获取档案数据失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, module_type):
        """添加模块项目"""
        try:
            user = request.user
            data = request.data
            
            # 获取对应的序列化器和模型
            serializer_map = {
                'basic_info': (BasicInfoSerializer, BasicInfo),
                'job_intention': (JobIntentionSerializer, JobIntention),
                'work_experience': (WorkExperienceSerializer, WorkExperience),
                'education': (EducationSerializer, Education),
                'project': (ProjectSerializer, Project),
                'skills': (SkillSerializer, Skill),  # 改回 'skills'
                'certificate': (CertificateSerializer, Certificate),
                'language': (LanguageSerializer, Language),
                'portfolio': (PortfolioSerializer, Portfolio),
                'social_link': (SocialLinkSerializer, SocialLink)
            }
            
            if module_type not in serializer_map:
                return Response({
                    'code': 400,
                    'message': '无效的模块类型'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            SerializerClass, ModelClass = serializer_map[module_type]
            
            # 创建新记录
            serializer = SerializerClass(data=data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({
                    'code': 200,
                    'message': '添加成功',
                    'data': serializer.data
                })
            
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"添加模块数据失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '添加失败',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, module_type, pk=None):
        """更新模块数据"""
        try:
            user = request.user
            data = request.data
            
            # 获取对应的序列化器和模型
            serializer_map = {
                'basic_info': (BasicInfoSerializer, BasicInfo),
                'job_intention': (JobIntentionSerializer, JobIntention),
                'work_experience': (WorkExperienceSerializer, WorkExperience),
                'education': (EducationSerializer, Education),
                'project': (ProjectSerializer, Project),
                'skills': (SkillSerializer, Skill),  # 确保这里是 'skills'
                'certificate': (CertificateSerializer, Certificate),
                'language': (LanguageSerializer, Language),
                'portfolio': (PortfolioSerializer, Portfolio),
                'social_link': (SocialLinkSerializer, SocialLink)
            }
            
            if module_type not in serializer_map:
                return Response({
                    'code': 400,
                    'message': '无效的模块类型'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            SerializerClass, ModelClass = serializer_map[module_type]
            
            # 特殊处理 basic_info（一对一关系）
            if module_type == 'basic_info':
                instance = ModelClass.objects.filter(user=user).first()
                if instance:
                    serializer = SerializerClass(instance, data=data, partial=True)
                else:
                    serializer = SerializerClass(data=data)
            else:
                # 其他模块的处理
                if pk:
                    instance = ModelClass.objects.filter(user=user, id=pk).first()
                    if not instance:
                        return Response({
                            'code': 404,
                            'message': '记录不存在'
                        }, status=status.HTTP_404_NOT_FOUND)
                    serializer = SerializerClass(instance, data=data, partial=True)
                else:
                    serializer = SerializerClass(data=data)
            
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({
                    'code': 200,
                    'message': '更新成功',
                    'data': serializer.data
                })
            
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"更新模块数据失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '更新失败',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, module_type, pk):
        """删除模块项目"""
        try:
            user = request.user
            
            # 获取对应的模型
            model_map = {
                'basic_info': BasicInfo,
                'job_intention': JobIntention,
                'work_experience': WorkExperience,
                'education': Education,
                'project': Project,
                'skills': Skill,  # 修改这里，使用 'skills'
                'certificate': Certificate,
                'language': Language,
                'portfolio': Portfolio,
                'social_link': SocialLink
            }
            
            if module_type not in model_map:
                return Response({
                    'code': 400,
                    'message': '无效的模块类型'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            ModelClass = model_map[module_type]
            
            # 查找并删除记录
            try:
                instance = ModelClass.objects.get(user=user, id=pk)
                instance.delete()
                return Response({
                    'code': 200,
                    'message': '删除成功'
                })
            except ModelClass.DoesNotExist:
                return Response({
                    'code': 404,
                    'message': '记录不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"删除模块数据失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '删除失败',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)