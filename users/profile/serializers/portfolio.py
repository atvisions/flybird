from rest_framework import serializers
from ..models.portfolio import Portfolio

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        exclude = ['user']
        read_only_fields = ['created_at', 'updated_at']
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type_display'] = instance.get_type_display()
        if instance.cover:
            ret['cover_url'] = instance.cover.url
        if instance.attachment:
            ret['attachment_url'] = instance.attachment.url
        return ret 