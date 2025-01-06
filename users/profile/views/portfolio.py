from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Portfolio
from ..serializers import PortfolioSerializer
import logging

logger = logging.getLogger(__name__)

class PortfolioView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取作品集列表"""
        try:
            portfolios = request.user.portfolios.all()
            serializer = PortfolioSerializer(portfolios, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in PortfolioView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """添加作品"""
        try:
            serializer = PortfolioSerializer(data=request.data)
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
            logger.error(f"Error in PortfolioView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PortfolioDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return user.portfolios.filter(pk=pk).first()
    
    def get(self, request, pk):
        """获取作品详情"""
        try:
            portfolio = self.get_object(pk, request.user)
            if not portfolio:
                return Response({
                    'code': 404,
                    'message': '作品不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PortfolioSerializer(portfolio)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in PortfolioDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        """更新作品"""
        try:
            portfolio = self.get_object(pk, request.user)
            if not portfolio:
                return Response({
                    'code': 404,
                    'message': '作品不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PortfolioSerializer(portfolio, data=request.data)
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
            logger.error(f"Error in PortfolioDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """删除作品"""
        try:
            portfolio = self.get_object(pk, request.user)
            if not portfolio:
                return Response({
                    'code': 404,
                    'message': '作品不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            portfolio.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            logger.error(f"Error in PortfolioDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 