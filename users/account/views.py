from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash, get_user_model
from .serializers import ChangePasswordSerializer, ChangePhoneSerializer
from ..utils.email import verify_email_code, send_verification_email, generate_email_code
import logging
import re

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

class BindEmailView(APIView):
    """绑定邮箱"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
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

class ChangeUsernameView(APIView):
    """修改用户名"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        username = request.data.get('username', '').strip()
        
        # 验证用户名格式
        if not re.match(r'^[a-zA-Z0-9\u4e00-\u9fa5]{2,20}$', username):
            return Response({
                'detail': '用户名只能包含字母、数字和汉字，长度2-20位'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 检查用户名是否已被使用
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            return Response({
                'detail': '该用户名已被使用'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 不允许使用纯数字的用户名
        if username.isdigit():
            return Response({
                'detail': '用户名不能是纯数字'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 更新用户名
        request.user.username = username
        request.user.save(update_fields=['username'])
        
        return Response({
            'message': '用户名修改成功',
            'username': username
        })
