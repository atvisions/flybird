from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.cache import cache
from ..models import User
from .serializers import RegisterSerializer, PasswordLoginSerializer, CodeLoginSerializer, ResetPasswordSerializer, ChangePhoneSerializer
from rest_framework_simplejwt.views import TokenRefreshView as JWTTokenRefreshView
import random
import re
from django.conf import settings
from ..utils.sms import send_sms
import logging
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """用户注册"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'code': 200,
                    'message': '注册成功',
                    'data': {
                        'tokens': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh)
                        }
                    }
                }, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                logger.error(f"Validation error during registration: {str(e)}")
                return Response({
                    'code': 400,
                    'message': str(e.detail[0]) if isinstance(e.detail, list) else str(e.detail),
                    'errors': e.detail
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Unexpected error during registration: {str(e)}")
                return Response({
                    'code': 500,
                    'message': '系统错误，请稍后重试',
                    'errors': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response({
            'code': 400,
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PasswordLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """密码登录"""
        serializer = PasswordLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.get_user()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # 获取过期时间（秒）
            access_expires_in = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            refresh_expires_in = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            
            print(f"Tokens generated: access={access_token}, refresh={str(refresh)}")  # 调试日志
            print(f"Expiry times: access={access_expires_in}s, refresh={refresh_expires_in}s")  # 调试日志
            
            return Response({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'tokens': {
                        'access': str(access_token),
                        'refresh': str(refresh),
                        'access_expires_in': int(access_expires_in),
                        'refresh_expires_in': int(refresh_expires_in)
                    }
                }
            })
        return Response({
            'code': 400,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        """退出登录"""
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'code': 200,
                'message': '退出成功'
            })
        except Exception:
            return Response({
                'code': 400,
                'message': '退出失败'
            }, status=status.HTTP_400_BAD_REQUEST)

class SendSmsCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """发送短信验证码"""
        phone = request.data.get('phone')
        scene = request.data.get('scene')  # register/login/reset/change_phone
        
        # 验证码类型映射
        scene_mapping = {
            'register': 'register',
            'login': 'login',
            'reset': 'reset_password',
            'change_phone': 'change_phone'
        }
        
        # 获取实际的验证码类型
        actual_scene = scene_mapping.get(scene)
        if not actual_scene:
            return Response({
                'code': 400,
                'message': '无效的场景类型'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if not phone:
            return Response({
                'code': 400,
                'message': '请提供手机号'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return Response({
                'code': 400,
                'message': '请输入正确的手机号'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 检查手机号是否已存在
        user_exists = User.objects.filter(phone=phone).exists()
        
        # 注册和更换手机号场景：手机号不能已存在
        if scene in ['register', 'change_phone'] and user_exists:
            return Response({
                'code': 400,
                'message': '该手机号已被使用'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 重置密码场景：手机号必须存在
        if scene == 'reset' and not user_exists:
            return Response({
                'code': 400,
                'message': '该手机号未注册'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查发送��率
        cache_key = f'sms_limit_{phone}'
        if cache.get(cache_key):
            return Response({
                'code': 400,
                'message': '发送太频繁，请稍后再试'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 生成验证码
        code = ''.join(random.choices('0123456789', k=6))
        
        # 保存验证码到缓存
        code_key = f'{actual_scene}_{phone}'
        cache.set(code_key, code, timeout=300)  # 5分钟有效期
        cache.set(cache_key, 1, timeout=60)     # 1分钟内不能重复发送
        
        # 添加调试日志
        logger.info(f"Storing SMS code: key={code_key}, code={code}")
        
        # 使用实际的短信服务
        if not settings.SMS_CONFIG['VIRTUAL_SMS']:
            try:
                success, error_msg = send_sms(phone, code, actual_scene)
                if not success:
                    logger.error(f"Failed to send SMS to {phone}: {error_msg}")
                    return Response({
                        'code': 400,
                        'message': f'发送失败: {error_msg}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"SMS service error: {str(e)}")
                return Response({
                    'code': 500,
                    'message': '短信服务异常，请稍后重试'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 根据配置决定是否返回验证码
        if settings.SMS_CONFIG['VIRTUAL_SMS'] or (settings.DEBUG and settings.SMS_CONFIG['SHOW_SMS_IN_DEBUG']):
            return Response({
                'code': 200,
                'message': '验证码已发送',
                'data': {
                    'code': code,
                    'cache_key': code_key
                }
            })
        
        return Response({
            'code': 200,
            'message': '验证码已发送'
        })

class CodeLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """验证码登录"""
        serializer = CodeLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.get_user()
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    },
                    'user': {
                        'id': user.id,
                        'phone': user.phone
                    },
                    'is_new_user': getattr(serializer, 'is_new_user', False)
                }
            })
        return Response({
            'code': 400,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(JWTTokenRefreshView):
    """刷新 Token"""
    permission_classes = [AllowAny]  # 允许未登录访问
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return Response({
                'code': 200,
                'message': 'Token刷新成功',
                'data': {
                    'access': response.data['access']
                }
            })
        except Exception as e:
            logger.error(f"Error in TokenRefreshView: {str(e)}", exc_info=True)
            return Response({
                'code': 400,
                'message': 'Token刷新失败',
                'errors': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    """重置密码"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': '密码重置成功'
                })
            return Response({
                'code': 400,
                'message': '密码重置失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in ResetPasswordView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePhoneView(APIView):
    """更换手机号"""
    
    def post(self, request):
        try:
            serializer = ChangePhoneSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save(user=request.user)
                return Response({
                    'code': 200,
                    'message': '手机号��换成功',
                    'data': {
                        'phone': user.phone
                    }
                })
            return Response({
                'code': 400,
                'message': '手机号更换失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in ChangePhoneView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_register_code(request):
    """发送注册验证码"""
    phone = request.data.get('phone')
    
    # 验证手机号格式
    if not re.match(r'^1[3-9]\d{9}$', phone):
        return Response({
            'code': 400,
            'message': '请输入有效的手机号'
        })
    
    # 检查手机号是否已注册
    if User.objects.filter(phone=phone).exists():
        return Response({
            'code': 400,
            'message': '该手机号已注册'
        })
    
    # 生成验证码
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    cache_key = f"register_{phone}"
    
    # 将验证码存入缓存，设置5分钟过期
    cache.set(cache_key, code, 300)
    
    # TODO: 在生产环境中，这里应该调用短信服务发送验证码
    # 开发环境直接返回验证码
    if settings.DEBUG:
        return Response({
            'code': 200,
            'message': '验证码已发送',
            'data': {
                'code': code,
                'cache_key': cache_key
            }
        })
    else:
        # 调用短信服务发送验证码
        try:
            # send_sms(phone, code)
            return Response({
                'code': 200,
                'message': '验证码已发送'
            })
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            return Response({
                'code': 500,
                'message': '验证码发送失败，请稍后重试'
            })
