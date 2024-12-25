from rest_framework import serializers
from django.core.cache import cache

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField(min_length=6)
    
    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return attrs

class ChangePhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    
    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        cached_code = cache.get(f'change_phone_{phone}')
        
        if not cached_code or cached_code != code:
            raise serializers.ValidationError("验证码无效或已过期")
            
        return attrs
