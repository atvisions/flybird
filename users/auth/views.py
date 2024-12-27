from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (
    PasswordLoginSerializer, RegisterSerializer,
    ResetPasswordSerializer, ChangePhoneSerializer
)
from users.utils.sms import send_sms
import random

User = get_user_model()

class PasswordLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': RegisterSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class SendSmsCodeView(APIView):
    # 根据场景设置权限
    def get_permissions(self):
        if self.request.data.get('scene') == 'change_phone':
            # 更换手机号需要登录
            return [permissions.IsAuthenticated()]
        # 其他场景（注册、登录、重置密码）不需要登录
        return [permissions.AllowAny()]
    
    VALID_SCENES = {
        'register': '注册',
        'login': '登录',
        'reset_password': '重置密码',
        'change_phone': '更换手机号'
    }
    
    def post(self, request):
        phone = request.data.get('phone')
        scene = request.data.get('scene')
        
        # 验证参数
        if not phone:
            return Response({'detail': '手机号不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        if not scene:
            return Response({'detail': '场景不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        if scene not in self.VALID_SCENES:
            return Response({'detail': '无效的场景类型'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 根据场景验证
        if scene == 'register':
            if User.objects.filter(phone=phone).exists():
                return Response({'detail': '该手机号已注册'}, status=status.HTTP_400_BAD_REQUEST)
        elif scene == 'change_phone':
            if User.objects.filter(phone=phone).exists():
                return Response({'detail': '该手机号已被使用'}, status=status.HTTP_400_BAD_REQUEST)
        elif scene in ['login', 'reset_password']:
            if not User.objects.filter(phone=phone).exists():
                return Response({'detail': '该手机号未注册'}, status=status.HTTP_400_BAD_REQUEST)
             
        # 生成验证码
        code = ''.join(random.choices('0123456789', k=6))
        
        # 保存验证码到缓存
        cache_key = f'sms_code_{scene}_{phone}'
        cache.set(cache_key, code, timeout=300)  # 5分钟有效期
        
        try:
            # 发送短信
            send_sms(phone, code, scene)
            
            # 根据配置决定是否显示验证码
            if settings.SMS_CONFIG.get('SHOW_SMS_IN_DEBUG', False):
                return Response({
                    'message': f'{self.VALID_SCENES[scene]}验证码已发送',
                    'code': code
                })
            # 不显示验证码时的响应
            return Response({
                'message': f'{self.VALID_SCENES[scene]}验证码已发送'
            })
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': '密码重置成功'})

class ChangePhoneView(APIView):
    def post(self, request):
        serializer = ChangePhoneSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': '手机号更换成功'})
