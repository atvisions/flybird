from rest_framework import serializers
from ..models.social import SocialLink

class SocialLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.SerializerMethodField()

    class Meta:
        model = SocialLink
        exclude = ['user']
        read_only_fields = ['created_at', 'updated_at']

    def get_platform_display(self, obj):
        """获取平台显示名称"""
        return dict(SocialLink.PLATFORM_CHOICES).get(obj.platform, obj.platform)