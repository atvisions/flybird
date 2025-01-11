from rest_framework import serializers
from .models import User
from membership.services import MembershipCacheService

class UserSerializer(serializers.ModelSerializer):
    vip_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'uid', 'username', 'phone', 'email', 'avatar',
            'background_image', 'position', 'bio', 'is_vip',
            'vip_type', 'vip_expire_time', 'vip_status', 'is_staff'
        ]
        read_only_fields = [
            'id', 'uid', 'phone', 'email', 'is_vip',
            'vip_type', 'vip_expire_time', 'vip_status'
        ] 

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'uid', 'username', 'phone', 'email', 'avatar',
            'background_image', 'position', 'bio', 'is_vip',
            'vip_type', 'vip_expire_time', 'vip_status', 'is_staff'
        ] 
