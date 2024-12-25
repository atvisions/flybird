from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import BasicInfo

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """用户基本信息序列化器"""
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'nickname',
            'email',
            'phone',
            'avatar',
            'is_active',
            'date_joined',  # 使用 date_joined 替代 created_at
            'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

class BasicInfoSerializer(serializers.ModelSerializer):
    """用户详细信息序列化器"""
    class Meta:
        model = BasicInfo
        exclude = ['user']  # 排除 user 字段，因为它会自动关联
        read_only_fields = ['id', 'created_at', 'updated_at']
