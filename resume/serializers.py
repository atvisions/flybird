from rest_framework import serializers
from .models import ResumeTemplate, Resume, Component, TemplateCategory, ComponentCategory, Component

class TemplateCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    template_count = serializers.SerializerMethodField()

    class Meta:
        model = TemplateCategory
        fields = [
            'id', 'name', 'icon', 'description', 'sort_order',
            'is_active', 'parent', 'children', 'template_count',
            'created_at', 'updated_at'
        ]

    def get_children(self, obj):
        if obj.children.exists():
            return TemplateCategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []

    def get_template_count(self, obj):
        return obj.templates.filter(status='approved').count()

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'name', 'type', 'icon', 'config', 'is_system', 'creator']
        read_only_fields = ['creator']

class ResumeTemplateSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()
    category_data = TemplateCategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = ResumeTemplate
        fields = [
            'id', 'name', 'thumbnail', 'description', 'creator',
            'category', 'category_data', 'status', 'is_vip',
            'content', 'created_at', 'updated_at', 'is_creator'
        ]
        read_only_fields = ['creator', 'status']

    def get_is_creator(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.creator_id == request.user.id
        return False

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

class ResumeSerializer(serializers.ModelSerializer):
    template_data = ResumeTemplateSerializer(source='template', read_only=True)
    
    class Meta:
        model = Resume
        fields = [
            'id', 'name', 'user', 'template', 'template_data',
            'content', 'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

    def validate_template(self, template):
        user = self.context['request'].user
        if template.is_vip and not user.is_vip:
            raise serializers.ValidationError("该模板仅VIP用户可用")
        return template 

class ComponentCategorySerializer(serializers.ModelSerializer):
    """组件分类序列化器"""
    class Meta:
        model = ComponentCategory
        fields = ['id', 'name', 'code', 'icon', 'description', 'sort_order']

class ComponentListSerializer(serializers.ModelSerializer):
    """组件列表序列化器"""
    class Meta:
        model = Component
        fields = ['id', 'name', 'type', 'icon', 'description', 'category']

class ComponentDetailSerializer(serializers.ModelSerializer):
    """组件详情序列化器"""
    class Meta:
        model = Component
        fields = ['id', 'name', 'type', 'icon', 'description', 'category', 
                 'config', 'template', 'preview_image'] 