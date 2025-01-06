from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.language import Language
from ..serializers import LanguageSerializer
import logging

logger = logging.getLogger(__name__)

class LanguageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取语言能力列表"""
        try:
            logger.info(f"Language GET request from user: {request.user}")
            languages = request.user.languages.all()
            serializer = LanguageSerializer(languages, many=True)
            logger.info(f"Found {languages.count()} languages")
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in LanguageView GET: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        """添加语言能力"""
        try:
            # 添加请求数据的日志
            logger.info(f"Language POST request data: {request.data}")
            
            serializer = LanguageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({
                    'code': 200,
                    'message': '添加成功',
                    'data': serializer.data
                })
            
            # 添加验证错误的日志
            logger.error(f"Language serializer validation errors: {serializer.errors}")
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # 添加详细的异常信息
            logger.error(f"Error in LanguageView POST: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LanguageDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return user.languages.filter(pk=pk).first()
    
    def get(self, request, pk):
        """获取语言能力详情"""
        try:
            language = self.get_object(pk, request.user)
            if not language:
                return Response({
                    'code': 404,
                    'message': '语言能力记录不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = LanguageSerializer(language)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in LanguageDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        """更新语言能力"""
        try:
            language = self.get_object(pk, request.user)
            if not language:
                return Response({
                    'code': 404,
                    'message': '语言能力记录不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = LanguageSerializer(language, data=request.data)
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
            logger.error(f"Error in LanguageDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """删除语言能力"""
        try:
            language = self.get_object(pk, request.user)
            if not language:
                return Response({
                    'code': 404,
                    'message': '语言能力记录不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            language.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            logger.error(f"Error in LanguageDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)