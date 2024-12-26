from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import WorkExperience, Project, ProfileScore
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ContentQualityView(APIView):
    """内容质量相关接口"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取内容质量评分和可优化字段"""
        try:
            score = request.user.profile_score
            from ..services.completeness import CompletenessCalculator
            calculator = CompletenessCalculator(request.user)
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'content_quality': {
                        'score': float(score.content_quality),
                        'status': calculator.get_content_quality_status(),
                        'optimize_fields': calculator.get_optimize_fields()
                    }
                }
            })
        except Exception as e:
            logger.error(f"Error in ContentQualityView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """更新AI优化后的内容"""
        try:
            field = request.data.get('field')
            content = request.data.get('content')
            quality_score = float(request.data.get('quality_score', 0))
            
            if not field or not content:
                return Response({
                    'code': 400,
                    'message': '缺少必要参数',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 更新内容
            if field == 'personal_summary':
                basic_info = request.user.basic_info
                basic_info.personal_summary = content
                basic_info.save()
            elif field.startswith('work_experience_'):
                work_id = field.split('_')[-1]
                work = WorkExperience.objects.get(id=work_id, user=request.user)
                work.description = content
                work.save()
            elif field.startswith('project_'):
                project_id = field.split('_')[-1]
                project = Project.objects.get(id=project_id, user=request.user)
                if 'description' in request.data:
                    project.description = request.data['description']
                if 'achievement' in request.data:
                    project.achievement = request.data['achievement']
                project.save()
            
            # 更新内容质量分数
            score = request.user.profile_score
            
            # 获取或初始化已优化字段列表
            optimized_fields = score.optimized_fields or []
            
            # 如果是新字段，添加到已优化列表
            if field not in optimized_fields:
                optimized_fields.append(field)
                score.optimized_fields = optimized_fields
            
            # 计算新的内容质量分数
            field_count = len(optimized_fields)
            if field_count == 1:
                # 第一个字段直接使用分数
                new_score = quality_score
            else:
                # 使用加权平均
                current_score = score.content_quality or 0
                new_score = (current_score * (field_count - 1) + quality_score) / field_count
            
            score.content_quality = round(new_score, 1)
            score.save()
            
            logger.info(f"更新内容质量分数 - 用户: {request.user.phone}")
            logger.info(f"字段: {field}")
            logger.info(f"当前分数: {score.content_quality}")
            logger.info(f"新分数: {quality_score}")
            logger.info(f"已优化字段: {optimized_fields}")
            logger.info(f"最终分数: {new_score}")
            
            return Response({
                'code': 200,
                'message': '内容更新成功',
                'data': {
                    'field': field,
                    'content_quality_score': score.content_quality,
                    'optimized_fields': score.optimized_fields
                }
            })
            
        except Exception as e:
            logger.error(f"Error in ContentQualityView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 