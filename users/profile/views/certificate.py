from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Certificate
from ..serializers import CertificateSerializer
import logging

logger = logging.getLogger(__name__)

class CertificateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取证书奖项列表"""
        try:
            certificates = request.user.certificates.all()
            serializer = CertificateSerializer(certificates, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in CertificateView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """添加证书奖项"""
        try:
            serializer = CertificateSerializer(data=request.data)
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
            logger.error(f"Error in CertificateView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CertificateDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return user.certificates.filter(pk=pk).first()
    
    def get(self, request, pk):
        """获取证书奖项详情"""
        try:
            certificate = self.get_object(pk, request.user)
            if not certificate:
                return Response({
                    'code': 404,
                    'message': '证书奖项不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CertificateSerializer(certificate)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in CertificateDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        """更新证书奖项"""
        try:
            certificate = self.get_object(pk, request.user)
            if not certificate:
                return Response({
                    'code': 404,
                    'message': '证书奖项不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CertificateSerializer(certificate, data=request.data)
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
            logger.error(f"Error in CertificateDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """删除证书奖项"""
        try:
            certificate = self.get_object(pk, request.user)
            if not certificate:
                return Response({
                    'code': 404,
                    'message': '证书奖项不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            certificate.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            logger.error(f"Error in CertificateDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 