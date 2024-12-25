from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import ProfileLayout
from ..serializers import ProfileLayoutSerializer
import logging

logger = logging.getLogger(__name__)

class ProfileLayoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取档案布局配置"""
        try:
            layout, created = ProfileLayout.objects.get_or_create(user=request.user)
            serializer = ProfileLayoutSerializer(layout)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in ProfileLayoutView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        """更新档案布局配置"""
        try:
            layout, created = ProfileLayout.objects.get_or_create(user=request.user)
            serializer = ProfileLayoutSerializer(layout, data=request.data)
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
            logger.error(f"Error in ProfileLayoutView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 