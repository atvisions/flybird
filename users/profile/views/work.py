from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import WorkExperience
from ..serializers import WorkExperienceSerializer
import logging

logger = logging.getLogger(__name__)

class WorkExperienceView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取工作经历列表"""
        try:
            experiences = request.user.work_experiences.all()
            serializer = WorkExperienceSerializer(experiences, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in WorkExperienceView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """添加工作经历"""
        try:
            serializer = WorkExperienceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
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
            logger.error(f"Error in WorkExperienceView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkExperienceDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return user.work_experiences.filter(pk=pk).first()
    
    def get(self, request, pk):
        """获取工作经历详情"""
        try:
            experience = self.get_object(pk, request.user)
            if not experience:
                return Response({
                    'code': 404,
                    'message': '工作经历不��在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = WorkExperienceSerializer(experience)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in WorkExperienceDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        """更新工作经历"""
        try:
            experience = self.get_object(pk, request.user)
            if not experience:
                return Response({
                    'code': 404,
                    'message': '工作经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = WorkExperienceSerializer(experience, data=request.data)
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
            logger.error(f"Error in WorkExperienceDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
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
            logger.error(f"Error in WorkExperienceDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 