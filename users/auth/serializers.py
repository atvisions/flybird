import re
import logging
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()
logger = logging.getLogger(__name__)

class RegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['phone', 'password', 'confirm_password', 'code']
        extra_kwargs = {
            'password': {'write_only': True},
            'phone': {'required': True}
        }

    def validate_phone(self, value):
        """验证手机号"""
        # 添加手机号格式验证
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('请输入有效的手机号')
            
        # 检查手机号是否已注册
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已注册')
            
        return value

    def validate(self, attrs):
        """验证密码和验证码"""
        # 验证密码
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次密码不一致'})
            
        # 验证码校验
        cache_key = f"register_{attrs['phone']}"
        cached_code = cache.get(cache_key)
        if not cached_code:
            raise serializers.ValidationError({'code': '验证码已过期'})
        if attrs['code'] != cached_code:
            raise serializers.ValidationError({'code': '验证码错误'})
            
        return attrs

    def create(self, validated_data):
        """创建用户"""
        try:
            # 移除不需要的字段
            validated_data.pop('code', None)
            validated_data.pop('confirm_password', None)
            
            # 创建用户
            user = User.objects.create_user(
                phone=validated_data['phone'],
                password=validated_data['password'],
                username=validated_data['phone']
            )
            
            # 清除验证码缓存
            cache_key = f"register_{validated_data['phone']}"
            cache.delete(cache_key)
            
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            if 'unique constraint' in str(e).lower():
                raise serializers.ValidationError('该手机号已被注册')
            else:
                raise serializers.ValidationError(f'注册失败: {str(e)}')

class PasswordLoginSerializer(serializers.Serializer):
    """密码登录序列化器"""
    phone = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        phone = attrs['phone']
        password = attrs['password']
        
        user = User.objects.filter(phone=phone).first()
        if not user:
            raise serializers.ValidationError("用户不存在")
            
        if not user.check_password(password):
            raise serializers.ValidationError("手机号或密码错误")
            
        self.user = user
        return attrs
        
    def get_user(self):
        return self.user

class CodeLoginSerializer(serializers.Serializer):
    """验证码登录序列化器"""
    phone = serializers.CharField()
    code = serializers.CharField()
    
    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        
        cached_code = cache.get(f'login_{phone}')
        if not cached_code or cached_code != code:
            raise serializers.ValidationError("验证码无效或已过期")
        
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'username': phone,
                'password': User.objects.make_random_password()
            }
        )
        
        self.user = user
        self.is_new_user = created
        return attrs
        
    def get_user(self):
        return self.user

class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, help_text='手机号')
    code = serializers.CharField(required=True, help_text='验证码')
    password = serializers.CharField(required=True, help_text='新密码')
    confirm_password = serializers.CharField(required=True, help_text='确认密码')

    def validate(self, data):
        """
        验证:
        1. 两次密码是否一致
        2. 验证码是否有效
        """
        # 验证两次密码是否一致
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('两次输入的密码不一致')

        # 验证验证码
        phone = data['phone']
        code = data['code']
        cached_code = cache.get(f'reset_password_{phone}')
        
        if not cached_code or cached_code != code:
            raise serializers.ValidationError('验证码无效或已过期')

        return data

    def save(self):
        phone = self.validated_data['phone']
        password = self.validated_data['password']
        
        try:
            user = User.objects.get(phone=phone)
            user.set_password(password)
            user.save()
            
            # 清除验证码缓存
            cache.delete(f'reset_password_{phone}')
            
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError('用户不存在')

class ChangePhoneSerializer(serializers.Serializer):
    new_phone = serializers.CharField(required=True, help_text='新手机号')
    code = serializers.CharField(required=True, help_text='验证码')

    def validate_new_phone(self, value):
        """验证新手机号"""
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('请输入有效的手机号')
            
        # 检查手机号是否已被使用
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已被使用')
            
        return value

    def validate(self, data):
        """验证验证码"""
        new_phone = data['new_phone']
        code = data['code']
        cached_code = cache.get(f'change_phone_{new_phone}')
        
        if not cached_code or cached_code != code:
            raise serializers.ValidationError('验证码无效或已过期')

        return data

    def save(self, user):
        new_phone = self.validated_data['new_phone']
        
        # 更新手机号
        user.phone = new_phone
        user.save()
        
        # 清除验证码缓存
        cache.delete(f'change_phone_{new_phone}')
        
        return user
