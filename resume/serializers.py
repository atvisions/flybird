from rest_framework import serializers
from .models import Resume
from template_editor.serializers import TemplateSerializer

class ResumeSerializer(serializers.ModelSerializer):
    """简历序列化器"""
    template_detail = TemplateSerializer(source='template', read_only=True)
    creator_name = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Resume
        fields = [
            'id', 'name', 'description', 'creator', 'creator_name',
            'template', 'template_detail', 'content', 'status',
            'is_public', 'view_count', 'download_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'view_count', 'download_count', 'created_at', 'updated_at']

    def validate_content(self, value):
        """验证简历内容的格式"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("简历内容必须是一个字典")
        return value

    def create(self, validated_data):
        """创建简历时自动设置创建者"""
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data) 