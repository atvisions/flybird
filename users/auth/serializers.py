import re
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
import logging

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

    def validate_account(self, value):
        # 验证账号格式
        # 手机号格式: 1开头的11位数字
        # 邮箱格式: 包含@的字符串
        # UID格式: 纯数字
        if not (
            re.match(r'^1[3-9]\d{9}$', value) or  # 手机号
            re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', value) or  # 邮箱
            re.match(r'^\d+$', value)  # UID
        ):
            raise serializers.ValidationError('请输入正确的手机号/邮箱/UID')
        return value

    def validate(self, attrs):
        account = attrs.get('account')
        password = attrs.get('password')

        try:
            # 根据不同格式查找用户
            if re.match(r'^1[3-9]\d{9}$', account):
                user = User.objects.get(phone=account)
            elif re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', account):
                # 确保邮箱不为空且已验证
                user = User.objects.get(email=account, email__isnull=False)
            elif re.match(r'^\d+$', account):
                # 移除前导零，因为 uid 格式是 1000000 + pk
                cleaned_uid = str(int(account))
                user = User.objects.get(uid=cleaned_uid)
            else:
                raise User.DoesNotExist
            
            if not user.check_password(password):
                raise serializers.ValidationError({
                    'password': ['密码错误，请重新输入']
                })
            
            if not user.is_active:
                raise serializers.ValidationError({
                    'account': ['该账号已被禁用，请联系客服']
                })
            
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'account': ['账号未注册，请先注册']
            })

        # 打印调试信息
        logger.info(f"Login attempt - Account: {account}, User found: {user.uid}")
        
        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)  # 新增确认密码字段
    code = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'confirm_password', 'code')  # 添加confirm_password到fields
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},  # 确保确认密码也是write_only
        }

    def validate(self, attrs):
        try:
            # 验证两次密码是否一致
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError({'confirm_password': '两次输入的密码不一致'})

            # 验证手机号是否已注册
            phone = attrs.get('phone')
            if User.objects.filter(phone=phone).exists():
                raise serializers.ValidationError({'phone': '该手机号已注册'})
                
            # 验证验证码 - 使用与发送验证码时相同的缓存key格式
            code = attrs.get('code')
            cache_key = f'sms_code_register_{phone}'  # 保持与发送时的格式一致
            cached_code = cache.get(cache_key)
            
            logger.info(f"注册验证 - 手机号: {phone}")
            logger.info(f"验证码比对 - 缓存key: {cache_key}, 输入: {code}, 缓存: {cached_code}")
            
            if not cached_code:
                raise serializers.ValidationError({'code': '验证码已过期'})
            if code != cached_code:
                raise serializers.ValidationError({'code': '验证码错误'})
                
            return attrs
            
        except Exception as e:
            logger.error(f"验证异常: {str(e)}", exc_info=True)
            raise

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
    new_password = serializers.CharField(validators=[validate_password])
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
                'phone': ['用户不存在']
            })

        # 验证两次密码是否一致
        if new_password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': ['两次输入的密码不一致']
            })

        # 验证短信验证码
        cache_key = f'sms_code_reset_password_{phone}'
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            raise serializers.ValidationError({
                'code': ['验证码已过期，请重新获取']
            })
            
        if code != cached_code:
            raise serializers.ValidationError({
                'code': ['验证码错误']
            })

        # 验证成功后删除缓存的验证码
        cache.delete(cache_key)
        
        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        # 记录密码重置日志
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
