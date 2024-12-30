from rest_framework import serializers
from ..models import ProfileLayout

class ProfileLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLayout
        fields = ['layout']

    def to_representation(self, instance):
        """自定义数据展示"""
        return {
            'code': 200,
            'message': '获取成功',
            'data': {
                'layout': instance.layout
            }
        } 