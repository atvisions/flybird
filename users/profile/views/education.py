from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Education
from ..serializers import EducationSerializer
import logging

logger = logging.getLogger(__name__)

class EducationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取教育经历列表"""
        try:
            educations = request.user.educations.all()
            serializer = EducationSerializer(educations, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in EducationView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """添加教育经历"""
        try:
            serializer = EducationSerializer(data=request.data)
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
            logger.error(f"Error in EducationView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EducationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return user.educations.filter(pk=pk).first()
    
    def get(self, request, pk):
        """获取教育经历详情"""
        try:
            education = self.get_object(pk, request.user)
            if not education:
                return Response({
                    'code': 404,
                    'message': '教育经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = EducationSerializer(education)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in EducationDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        """更新教育经历"""
        try:
            education = self.get_object(pk, request.user)
            if not education:
                return Response({
                    'code': 404,
                    'message': '教育经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = EducationSerializer(education, data=request.data)
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
            logger.error(f"Error in EducationDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """删除教育经历"""
        try:
            education = self.get_object(pk, request.user)
            if not education:
                return Response({
                    'code': 404,
                    'message': '教育经历不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            education.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            logger.error(f"Error in EducationDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 