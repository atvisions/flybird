from rest_framework import serializers
from ..models.social import SocialLink

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        exclude = ['user']
        read_only_fields = ['created_at', 'updated_at']
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['platform_display'] = instance.get_platform_display()
        return ret
