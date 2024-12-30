from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from ..models import WorkExperience
from ..serializers.work import WorkExperienceSerializer
import logging
import traceback

logger = logging.getLogger(__name__)

class WorkExperienceView(APIView):
    """工作经历列表视图"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取工作经历列表"""
        try:
            logger.info(f"获取用户 {request.user.phone} 的工作经历列表")
            
            # 获取数据
            experiences = WorkExperience.objects.filter(
                user=request.user
            ).order_by('-start_date')
            
            # 记录原始数据
            logger.info(f"原始数据: {list(experiences.values())}")
            
            # 序列化
            serializer = WorkExperienceSerializer(experiences, many=True)
            logger.info(f"序列化数据: {serializer.data}")
            
            # 构造响应
            response_data = {
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            }
            logger.info(f"响应数据: {response_data}")
            
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"获取工作经历失败: {str(e)}")
            logger.error(f"错误详情: {traceback.format_exc()}")
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """添加工作经历"""
        try:
            with transaction.atomic():
                serializer = WorkExperienceSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response({
                        'code': 200,
                        'message': '添加成功',
                        'data': serializer.data
                    })
                
            # 记录验证错误
            logger.error(f"数据验证失败: {serializer.errors}")
            
            # 格式化验证错误信息
            errors = {}
            for field, error_list in serializer.errors.items():
                errors[field] = [str(error) for error in error_list]
                
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"添加工作经历失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkExperienceDetailView(APIView):
    """工作经历详情视图"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return WorkExperience.objects.get(pk=pk, user=user)
        except WorkExperience.DoesNotExist:
            return None
    
    def put(self, request, pk):
        """更新工作经历"""
        try:
            experience = self.get_object(pk, request.user)
            if not experience:
                return Response({
                    'code': 404,
                    'message': '工作经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
                
            serializer = WorkExperienceSerializer(
                experience,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
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
            logger.error(f"更新工作经历失败: {str(e)}")
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """删除工作经历"""
        try:
            experience = self.get_object(pk, request.user)
            if not experience:
                return Response({
                    'code': 404,
                    'message': '工作经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
                
            experience.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            logger.error(f"删除工作经历失败: {str(e)}")
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 