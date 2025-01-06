from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.conf import settings
from rest_framework import permissions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users.models import ProfileScore
from .serializers import (
    PasswordLoginSerializer, RegisterSerializer,
    ResetPasswordSerializer, ChangePhoneSerializer
)
from users.utils.sms import send_sms
import random
import logging

logger = logging.getLogger('users')

User = get_user_model()

class PasswordLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # 打印请求数据以便调试
            print(f"Login request data: {request.data}")
            
            serializer = PasswordLoginSerializer(data=request.data)
            
            try:
                serializer.is_valid(raise_exception=True)
            except serializers.ValidationError as e:
                # 格式化验证错误信息
                error_messages = []
                for field, errors in e.detail.items():
                    if field == 'non_field_errors':
                        error_messages.extend(errors)
                    else:
                        error_messages.extend([f"{error}" for error in errors])
                
                return Response({
                    'code': 400,
                    'message': error_messages[0] if error_messages else '验证失败',
                    'errors': e.detail
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            # 打印成功登录信息
            print(f"User logged in successfully - UID: {user.uid}")
            
            return Response({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
            
        except Exception as e:
            # 打印详细的错误信息
            print(f"Login error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return Response({
                'code': 500,
                'message': f'登录失败：{str(e)}',
                'detail': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # 记录请求数据（排除敏感信息）
            safe_data = {
                'phone': request.data.get('phone'),
                'has_code': bool(request.data.get('code')),
                'has_password': bool(request.data.get('password')),
                'has_confirm_password': bool(request.data.get('confirm_password'))
            }
            logger.info(f"注册请求数据: {safe_data}")
            
            # 预检查密码匹配
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            if password != confirm_password:
                return Response({
                    'code': 400,
                    'message': '两次输入的密码不一致',
                    'errors': {
                        'confirm_password': ['两次输入的密码不一致']
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # 记录验证后的数据（排除敏感信息）
            safe_validated_data = {
                'phone': serializer.validated_data.get('phone'),
                'has_code': bool(serializer.validated_data.get('code'))
            }
            logger.info(f"验证后的数据: {safe_validated_data}")
            
            # 创建用户 - uid 和 username 会在 save() 方法中自动生成
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"用户创建成功: {user.phone}")
            
            # 直接返回用户信息
            return Response({
                'code': 200,
                'message': '注册成功',
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
            
        except serializers.ValidationError as e:
            # 处理验证错误，提供更友好的错误消息
            errors = e.detail
            message = '验证失败'
            
            if 'phone' in errors:
                message = str(errors['phone'][0])
            elif 'code' in errors:
                message = str(errors['code'][0])
            elif 'password' in errors:
                message = str(errors['password'][0])
            elif 'confirm_password' in errors:
                message = str(errors['confirm_password'][0])
            
            logger.warning(f"注册验证失败: {errors}")
            return Response({
                'code': 400,
                'message': message,
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"注册异常: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '注册失败，请稍后重试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
    permission_classes = [AllowAny]
    
    VALID_SCENES = {
        'register': '注册',
        'login': '登录',
        'reset_password': '重置密码',
        'change_phone': '更换手机号'
    }
    
    def post(self, request):
        try:
            # 获取参数
            phone = request.data.get('phone')
            scene = request.data.get('scene')
            
            # 记录请求信息
            logger.info(f"发送验证码请求 - 手机号: {phone}, 场景: {scene}")
            
            # 验证参数
            if not phone:
                return Response({
                    'code': 400,
                    'message': '手机号不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if not scene:
                return Response({
                    'code': 400,
                    'message': '场景不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if scene not in self.VALID_SCENES:
                return Response({
                    'code': 400,
                    'message': '无效的场景类型'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 根据场景验证
            if scene == 'register':
                if User.objects.filter(phone=phone).exists():
                    return Response({
                        'code': 400,
                        'message': '该手机号已注册'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif scene == 'change_phone':
                if User.objects.filter(phone=phone).exists():
                    return Response({
                        'code': 400,
                        'message': '该手机号已被使用'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif scene in ['login', 'reset_password']:
                if not User.objects.filter(phone=phone).exists():
                    return Response({
                        'code': 400,
                        'message': '该手机号未注册'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # 生成验证码
            code = ''.join(random.choices('0123456789', k=6))
            
            # 保存验证码到缓存
            cache_key = f'sms_code_{scene}_{phone}'
            cache.set(cache_key, code, timeout=300)  # 5分钟有效期
            
            # 验证是否存储成功
            stored_code = cache.get(cache_key)
            logger.info(f"验证码存储确认 - Key: {cache_key}, Code: {code}, Stored: {stored_code}")
            
            # 发送短信
            try:
                send_sms(phone, code, scene)
                logger.info(f"验证码发送成功 - 手机号: {phone}, 验证码: {code}")
                
                return Response({
                    'code': 200,
                    'message': f'{self.VALID_SCENES[scene]}验证码已发送',
                    'data': {
                        'code': code if settings.DEBUG else None
                    }
                })
                
            except Exception as e:
                logger.error(f"发送短信失败: {str(e)}", exc_info=True)
                return Response({
                    'code': 500,
                    'message': '发送验证码失败，请稍后重试'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"发送验证码异常: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
