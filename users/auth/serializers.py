from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache

User = get_user_model()

class PasswordLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not (username or phone):
            raise serializers.ValidationError('用户名或手机号必须提供一个')

        try:
            if username:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户不存在')

        if not user.check_password(password):
            raise serializers.ValidationError('密码错误')

        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    code = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('id', 'phone', 'password', 'code')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        # 验证手机号是否已注册
        phone = attrs.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({'phone': '该手机号已注册'})
            
        # 验证验证码
        code = attrs.get('code')
        cached_code = cache.get(f'sms_code_register_{phone}')
        
        if not cached_code:
            raise serializers.ValidationError({'code': '验证码已过期'})
        if code != cached_code:
            raise serializers.ValidationError({'code': '验证码错误'})
            
        return attrs

    def create(self, validated_data):
        # 移除验证码
        validated_data.pop('code', None)
        
        # 创建用户
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
        )
        
        return user

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

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
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
