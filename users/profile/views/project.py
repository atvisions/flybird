from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Project
from ..serializers import ProjectSerializer
import logging

logger = logging.getLogger(__name__)

class ProjectView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取项目经历列表"""
        try:
            projects = request.user.projects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in ProjectView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """添加项目经历"""
        try:
            serializer = ProjectSerializer(data=request.data)
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
            logger.error(f"Error in ProjectView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return user.projects.filter(pk=pk).first()
    
    def get(self, request, pk):
        """获取项目经历详情"""
        try:
            project = self.get_object(pk, request.user)
            if not project:
                return Response({
                    'code': 404,
                    'message': '项目经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProjectSerializer(project)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in ProjectDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        """更新项目经历"""
        try:
            project = self.get_object(pk, request.user)
            if not project:
                return Response({
                    'code': 404,
                    'message': '项目经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProjectSerializer(project, data=request.data)
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
            logger.error(f"Error in ProjectDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """删除项目经历"""
        try:
            project = self.get_object(pk, request.user)
            if not project:
                return Response({
                    'code': 404,
                    'message': '项目经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            project.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            logger.error(f"Error in ProjectDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 