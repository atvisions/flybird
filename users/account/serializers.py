from rest_framework import serializers
from django.core.cache import cache

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('当前密码错误，请重新输入')
        return value

    def validate_new_password(self, value):
    # 密码格式验证
        if len(value) < 8 or len(value) > 20:
            raise serializers.ValidationError('密码长度必须在8-20位之间')
        
        if not any(c.isalpha() for c in value):
            raise serializers.ValidationError('密码必须包含字母')
            
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError('密码必须包含数字')
                
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': '两次输入的密码不一致'
            })
            
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({
                'new_password': '新密码不能与当前密码相同'
            })
            
        return data


class ChangePhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    
    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        
        # 使用与发送验证码时相同的缓存key格式
        cache_key = f'sms_code_change_phone_{phone}'
        cached_code = cache.get(cache_key)
        
        if not cached_code or cached_code != code:
            raise serializers.ValidationError("验证码无效或已过期")
            
        return attrs

    def save(self, **kwargs):
        phone = self.validated_data['phone']
        user = self.context['request'].user
        user.phone = phone
        user.save(update_fields=['phone'])