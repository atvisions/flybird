from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import SocialLink
from ..serializers import SocialLinkSerializer
import logging

logger = logging.getLogger(__name__)

class SocialLinkView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取社交主页列表"""
        try:
            social_links = request.user.social_links.all()
            serializer = SocialLinkSerializer(social_links, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in SocialLinkView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """添加社交主页"""
        try:
            serializer = SocialLinkSerializer(data=request.data)
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
            logger.error(f"Error in SocialLinkView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SocialLinkDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return user.social_links.filter(pk=pk).first()
    
    def get(self, request, pk):
        """获取社交主页详情"""
        try:
            social_link = self.get_object(pk, request.user)
            if not social_link:
                return Response({
                    'code': 404,
                    'message': '社交主页不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = SocialLinkSerializer(social_link)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in SocialLinkDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        """更新社交主页"""
        try:
            social_link = self.get_object(pk, request.user)
            if not social_link:
                return Response({
                    'code': 404,
                    'message': '社交主页不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = SocialLinkSerializer(social_link, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': '更新成功',
                    'data': serializer.data
                })
            return Response({
                'code': 400,
                'message': '数��验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in SocialLinkDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """删除社交主页"""
        try:
            social_link = self.get_object(pk, request.user)
            if not social_link:
                return Response({
                    'code': 404,
                    'message': '社交主页不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            social_link.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            logger.error(f"Error in SocialLinkDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 