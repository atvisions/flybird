from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer, ChangePhoneSerializer
import logging

logger = logging.getLogger(__name__)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """修改密码"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)  # 更新session，避免退出登录
            return Response({
                'code': 200,
                'message': '密码修改成功'
            })
        return Response({
            'code': 400,
            'message': '密码修改失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ChangePhoneView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """修改手机号"""
        serializer = ChangePhoneSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.phone = serializer.validated_data['phone']
            user.save()
            return Response({
                'code': 200,
                'message': '手机号修改成功'
            })
        return Response({
            'code': 400,
            'message': '手机号修改失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    """删除账号"""
    permission_classes = [IsAuthenticated]  # 确保用户已登录
    
    def post(self, request):
        try:
            user = request.user
            
            # 验证密码
            password = request.data.get('password')
            if not user.check_password(password):
                return Response({
                    'code': 400,
                    'message': '密码错误'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 删除用户
            user.delete()
            
            return Response({
                'code': 200,
                'message': '账号已删除'
            })
        except Exception as e:
            logger.error(f"Delete account failed: {str(e)}")
            return Response({
                'code': 500,
                'message': '删除账号失败，请稍后重试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
