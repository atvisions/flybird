from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.intention import JobIntention
from ..serializers import JobIntentionSerializer
import logging

logger = logging.getLogger(__name__)

class JobIntentionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取求职意向"""
        try:
            intention = request.user.job_intention
            serializer = JobIntentionSerializer(intention)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in JobIntentionView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        """更新求职意向"""
        try:
            intention = request.user.job_intention
            serializer = JobIntentionSerializer(intention, data=request.data)
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
            logger.error(f"Error in JobIntentionView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 