from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash, get_user_model
from .serializers import ChangePasswordSerializer, ChangePhoneSerializer
from ..utils.email import verify_email_code, send_verification_email, generate_email_code
import logging
import re
from django.db import IntegrityError
from django.core.cache import cache
from ..models import User

logger = logging.getLogger(__name__)
User = get_user_model()

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
            
        # 构建更明确的错误信息
        error_messages = []
        for field, errors in serializer.errors.items():
            if isinstance(errors, list):
                error_messages.extend(errors)
            elif isinstance(errors, dict):
                for error in errors.values():
                    error_messages.extend(error)
                    
        return Response({
            'code': 400,
            'message': error_messages[0] if error_messages else '密码修改失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ChangePhoneView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            logger.info(f"Received change phone request - data: {request.data}")
            
            serializer = ChangePhoneSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                logger.error(f"Validation failed - errors: {serializer.errors}")
                return Response({
                    'detail': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            
            # 验证码校验
            cache_key = f'sms_code_change_phone_{phone}'
            cached_code = cache.get(cache_key)
            logger.info(f"Validating code - cached: {cached_code}, received: {code}")
            
            if not cached_code:
                return Response({
                    'detail': '验证码已过期，请重新获取'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if cached_code != code:
                return Response({
                    'detail': '验证码错误'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查手机号是否已被使用
            if User.objects.filter(phone=phone).exclude(id=request.user.id).exists():
                return Response({
                    'detail': '该手机号已被其他用户使用'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 更新手机号
            user = request.user
            user.phone = phone
            user.save(update_fields=['phone'])
            
            # 清除验证码缓存
            cache.delete(cache_key)
            
            return Response({
                'code': 200,
                'message': '手机号修改成功'
            })
            
        except Exception as e:
            logger.error(f"Change phone failed - error: {str(e)}")
            return Response({
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

class BindEmailView(APIView):
    """绑定邮箱"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        password = request.data.get('password')
        
        # 验证密码
        if not request.user.check_password(password):
            return Response({
                'detail': '密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证邮箱格式
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return Response({'detail': '邮箱格式不正确'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证验证码
        if not verify_email_code(email, code):
            return Response({'detail': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 检查邮箱是否已被使用
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            return Response({'detail': '该邮箱已被使用'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 绑定邮箱
        request.user.email = email
        request.user.save(update_fields=['email'])
        
        return Response({'message': '邮箱绑定成功'})

class SendEmailCodeView(APIView):
    """发送邮箱验证码"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        logger.info(f"Received request to send email code for user {request.user.username}")
        logger.info(f"Email: {email}")
        
        # 验证密码
        if not request.user.check_password(password):
            logger.error(f"Password validation failed for user {request.user.username}")
            return Response({
                'detail': '密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        logger.info(f"Password validation successful for user {request.user.username}")
        
        # 验证邮箱格式
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return Response({'detail': '邮箱格式不正确'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 检查邮箱是否已被使用
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            return Response({'detail': '该邮箱已被使用'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 生成并发送验证码
        try:
            code = generate_email_code()
            send_verification_email(email, code)
            return Response({'message': '验证码已发送'})
        except Exception as e:
            logger.error(f"发送邮箱验证码失败: {str(e)}")
            return Response({'detail': '验证码发送失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnbindEmailView(APIView):
    """解除邮箱绑定"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # 验证密码
        password = request.data.get('password')
        if not request.user.check_password(password):
            return Response({
                'detail': '密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 解除绑定
        request.user.email = ''
        request.user.save(update_fields=['email'])
        
        return Response({
            'message': '邮箱解绑成功'
        })

class ChangeEmailView(APIView):
    """更换邮箱"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        password = request.data.get('password')
        
        # 验证密码
        if not request.user.check_password(password):
            return Response({
                'detail': '密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证邮箱格式
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return Response({
                'detail': '邮箱格式不正确'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证验证码
        if not verify_email_code(email, code):
            return Response({
                'detail': '验证码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 检查邮箱是否已被使用
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            return Response({
                'detail': '该邮箱已被使用'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 更换邮箱
        request.user.email = email
        request.user.save(update_fields=['email'])
        
        return Response({
            'message': '邮箱更换成功'
        })


    """修改用户名"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            username = request.data.get('username')
            
            if not username:
                return Response({
                    'code': 400,
                    'message': '昵称不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 更新用户昵称
            user = request.user
            user.username = username
            user.save()
            
            return Response({
                'code': 200,
                'message': '昵称修改成功',
                'data': {
                    'username': username
                }
            })
            
        except Exception as e:
            logger.error(f"更新昵称失败: {str(e)}")
            return Response({
                'code': 500,
                'message': '修改昵称失败'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)