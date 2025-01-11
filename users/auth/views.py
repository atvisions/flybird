from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.conf import settings
from rest_framework import permissions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import ProfileScore
from .serializers import (
    PasswordLoginSerializer, RegisterSerializer,
    ResetPasswordSerializer, ChangePhoneSerializer
)
from users.utils.sms import send_sms
from users.utils.email import verify_email_code, send_verification_email, generate_email_code
import random
import logging
import re

from django_redis import get_redis_connection
from redis.exceptions import RedisError
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
        'reset_password': '重置密码',
        'change_phone': '更换手机号'
    }

    def post(self, request):
        try:
            phone = request.data.get('phone')
            scene = request.data.get('scene', 'default')
            
            # 验证手机号
            if not phone:
                return Response({
                    'code': 400,
                    'message': '手机号不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if not re.match(r'^1[3-9]\d{9}$', phone):
                return Response({
                    'code': 400,
                    'message': '手机号格式不正确'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 检查场景是否有效
            if scene not in self.VALID_SCENES:
                return Response({
                    'code': 400,
                    'message': '无效的场景'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 根据场景验证手机号
            if scene == 'register':
                if User.objects.filter(phone=phone).exists():
                    return Response({
                        'code': 400,
                        'message': '该手机号已注册'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif scene == 'reset_password':
                if not User.objects.filter(phone=phone).exists():
                    return Response({
                        'code': 400,
                        'message': '该手机号未注册'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # 使用缓存检查发送频率
            cache_key = f'sms_cooldown_{scene}_{phone}'
            if cache.get(cache_key):
                return Response({
                    'code': 429,
                    'message': '发送太频繁，请稍后再试'
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

            # 根据环境选择验证码
            use_virtual_sms = settings.DEBUG and settings.SMS_CONFIG.get('USE_VIRTUAL_SMS', False)
            if use_virtual_sms:
                code = settings.SMS_CONFIG.get('VIRTUAL_SMS_CODE', '123456')
                logger.info(f"使用虚拟验证码: {code}")
            else:
                code = ''.join(random.choices('0123456789', k=6))
                # TODO: 实际发送短信的代码
                # send_sms(phone, code, scene)

            # 保存验证码到缓存
            code_key = f'sms_code_{scene}_{phone}'
            cache.set(code_key, code, timeout=settings.SMS_CONFIG.get('SMS_EXPIRE_SECONDS', 300))
            # 设置冷却时间
            cache.set(cache_key, True, timeout=settings.SMS_CONFIG.get('SMS_COOLDOWN_SECONDS', 60))

            # 返回响应
            response_data = {
                'code': 200,
                'message': f'{self.VALID_SCENES[scene]}验证码已发送'
            }
            
            # 在开发环境中返回验证码
            if use_virtual_sms:
                response_data['data'] = {'code': code}

            return Response(response_data)

        except Exception as e:
            logger.error(f"发送验证码失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '发送验证码失败，请稍后重试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()  # 调用序列化器的 save 方法重置密码
                logger.info(f"密码重置成功 - Phone: {user.phone}")
                return Response({
                    'code': 200,
                    'message': '密码重置成功'
                })
            else:
                logger.warning(f"密码重置验证失败: {serializer.errors}")
                # 获取第一个错误信息
                first_error = next(iter(serializer.errors.values()))[0]
                return Response({
                    'code': 400,
                    'message': str(first_error)
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"密码重置异常: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '密码重置失败，请稍后重试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePhoneView(APIView):
    def post(self, request):
        serializer = ChangePhoneSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': '手机号更换成功'})

class ChangeEmailView(APIView):
    """更换邮箱"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
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
