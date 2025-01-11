import re
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
import logging
from django_redis import get_redis_connection
from redis.exceptions import RedisError
from django.conf import settings

logger = logging.getLogger('users')

User = get_user_model()

class PasswordLoginSerializer(serializers.Serializer):
    account = serializers.CharField(
        error_messages={
            'required': '请输入账号',
            'blank': '账号不能为空'
        }
    )
    password = serializers.CharField(
        error_messages={
            'required': '请输入密码',
            'blank': '密码不能为空'
        }
    )

    def validate(self, attrs):
        account = attrs.get('account')
        password = attrs.get('password')
        logger.info(f"开始验证登录 - Account: {account}")

        try:
            # 先尝试使用手机号查找
            if re.match(r'^1[3-9]\d{9}$', account):
                logger.info(f"使用手机号格式验证: {account}")
                try:
                    # 打印所有用户的手机号，用于调试
                    all_phones = list(User.objects.values_list('phone', flat=True))
                    logger.info(f"数据库中的所有手机号: {all_phones}")
                    
                    # 使用 filter().first() 代替 get()，并打印 SQL 查询
                    user = User.objects.filter(phone=account).first()
                    if not user:
                        logger.warning(f"手机号未注册: {account}")
                        raise User.DoesNotExist()
                    
                    logger.info(f"找到用户 - Phone: {account}, UID: {user.uid}")
                except User.DoesNotExist:
                    logger.warning(f"手机号未注册: {account}")
                    raise serializers.ValidationError({
                        'account': ['该手机号未注册']
                    })
            # 再尝试使用邮箱查找
            elif re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', account):
                logger.info(f"使用邮箱格式验证: {account}")
                try:
                    user = User.objects.get(email=account, email__isnull=False)
                    logger.info(f"找到用户 - Email: {account}, UID: {user.uid}")
                except User.DoesNotExist:
                    logger.warning(f"邮箱未注册: {account}")
                    raise serializers.ValidationError({
                        'account': ['该邮箱未注册']
                    })
            # 最后尝试使用 UID 查找（且不是手机号格式）
            elif re.match(r'^\d+$', account) and not re.match(r'^1[3-9]\d{9}$', account):
                logger.info(f"使用UID格式验证: {account}")
                cleaned_uid = str(int(account))
                try:
                    user = User.objects.get(uid=cleaned_uid)
                    logger.info(f"找到用户 - UID: {cleaned_uid}")
                except User.DoesNotExist:
                    logger.warning(f"UID未注册: {cleaned_uid}")
                    raise serializers.ValidationError({
                        'account': ['该UID未注册']
                    })
            else:
                logger.warning(f"无效的账号格式: {account}")
                raise User.DoesNotExist
            
            if not user.check_password(password):
                logger.warning(f"密码错误 - Account: {account}")
                raise serializers.ValidationError({
                    'password': ['密码错误，请重新输入']
                })
            
            if not user.is_active:
                logger.warning(f"账号已禁用 - Account: {account}")
                raise serializers.ValidationError({
                    'account': ['该账号已被禁用，请联系客服']
                })
            
            logger.info(f"登录验证成功 - Account: {account}, UID: {user.uid}")
            attrs['user'] = user
            return attrs
            
        except User.DoesNotExist:
            logger.warning(f"账号格式无效: {account}")
            raise serializers.ValidationError({
                'account': ['请输入正确的手机号/邮箱/UID']
            })

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', attrs['phone']):
            raise serializers.ValidationError({'phone': '手机号格式不正确'})

        # 验证验证码
        phone = attrs['phone']
        code = attrs['code']
        
        # 从缓存中获取验证码
        cache_key = f'sms_code_register_{phone}'
        cached_code = cache.get(cache_key)
        
        # 在开发环境中，如果是测试模式，使用固定的验证码
        if settings.DEBUG and settings.SMS_CONFIG.get('USE_VIRTUAL_SMS', False):
            if code != settings.SMS_CONFIG.get('VIRTUAL_SMS_CODE', '123456'):
                raise serializers.ValidationError({'code': '验证码错误'})
        else:
            if not cached_code:
                raise serializers.ValidationError({'code': '验证码已过期'})
            
            if cached_code != code:
                raise serializers.ValidationError({'code': '验证码错误'})

        # 验证密码
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({'password': '密码长度不能小于8位'})

        # 验证两次密码是否一致
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次输入的密码不一致'})

        return attrs

    def create(self, validated_data):
        try:
            # 移除验证码和确认密码字段
            validated_data.pop('code', None)
            validated_data.pop('confirm_password', None)  # 新增：移除确认密码字段
            
            # 创建用户
            user = User.objects.create_user(
                phone=validated_data['phone'],
                password=validated_data['password']
            )
            
            # 删除验证码缓存 - 使用与发送验证码时相同的缓存key格式
            cache_key = f'sms_code_register_{user.phone}'
            cache.delete(cache_key)
            
            logger.info(f"用户创建成功: {user.phone}")
            return user
            
        except Exception as e:
            logger.error(f"创建用户异常: {str(e)}", exc_info=True)
            raise

class PhoneLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户不存在')

        # TODO: 验证短信验证码
        
        attrs['user'] = user
        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # 验证用户是否存在
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'phone': '该手机号未注册'
            })

        # 验证验证码
        cache_key = f'sms_code_reset_password_{phone}'
        cached_code = cache.get(cache_key)
        
        # 开发环境验证码处理
        if settings.DEBUG and settings.SMS_CONFIG.get('USE_VIRTUAL_SMS', False):
            if code != settings.SMS_CONFIG.get('VIRTUAL_SMS_CODE', '123456'):
                raise serializers.ValidationError({'code': '验证码错误'})
        else:
            if not cached_code:
                raise serializers.ValidationError({'code': '验证码已过期'})
                
            if code != cached_code:
                raise serializers.ValidationError({'code': '验证码错误'})

        # 验证密码
        if len(new_password) < 8:
            raise serializers.ValidationError({
                'new_password': '密码长度不能小于8位'
            })

        # 验证两次密码是否一致
        if new_password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': '两次输入的密码不一致'
            })

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        
        # 设置新密码
        user.set_password(new_password)
        user.save()
        
        # 删除验证码缓存
        cache_key = f'sms_code_reset_password_{user.phone}'
        cache.delete(cache_key)
        
        logger.info(f"用户 {user.phone} 重置密码成功")
        return user

class ChangePhoneSerializer(serializers.Serializer):
    new_phone = serializers.CharField()
    code = serializers.CharField()

    def validate_new_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已被使用')
        return value

    def validate(self, attrs):
        # 验证验证码
        new_phone = attrs.get('new_phone')
        code = attrs.get('code')
        cached_code = cache.get(f'sms_code_change_phone_{new_phone}')
        
        if not cached_code:
            raise serializers.ValidationError('验证码已过期')
        if code != cached_code:
            raise serializers.ValidationError('验证码错误')
            
        return attrs

    def save(self):
        user = self.context['request'].user
        new_phone = self.validated_data['new_phone']
        user.phone = new_phone
        user.save()
        
        # 删除验证码缓存
        cache.delete(f'sms_code_change_phone_{new_phone}')
        return user
