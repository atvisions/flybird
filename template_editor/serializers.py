from rest_framework import serializers
from .models import Category, Template

class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value):
        """验证分类名称的唯一性"""
        if self.instance is None:  # 创建新分类时
            if Category.objects.filter(name=value).exists():
                raise serializers.ValidationError("该分类名称已存在")
        else:  # 更新分类时
            if Category.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("该分类名称已存在")
        return value

    def validate_sort_order(self, value):
        """验证排序值为非负数"""
        if value < 0:
            raise serializers.ValidationError("排序值不能为负数")
        return value 

class TemplateSerializer(serializers.ModelSerializer):
    """模板序列化器"""
    class Meta:
        model = Template
        fields = [
            'id', 'name', 'description', 'thumbnail', 'category',
            'keywords', 'creator', 'is_public', 'status', 'pages',
            'created_at', 'updated_at', 'views', 'likes', 'is_liked',
            'is_recommended'
        ]
        read_only_fields = ['creator', 'views', 'likes', 'is_liked']

    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.liked_by.all()
        return False

    def validate_name(self, value):
        """验证模板名称的唯一性"""
        if self.instance is None:  # 创建新模板时
            if Template.objects.filter(name=value).exists():
                raise serializers.ValidationError("该模板名称已存在")
        else:  # 更新模板时
            if Template.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("该模板名称已存在")
        return value

    def validate_pages(self, value):
        """验证页面数据的格式"""
        if not isinstance(value, list):
            raise serializers.ValidationError("pages 必须是一个列表")
        
        for page in value:
            if not isinstance(page, dict):
                raise serializers.ValidationError("每个页面必须是一个字典")
            
            if 'page_index' not in page:
                raise serializers.ValidationError("每个页面必须包含 page_index")
            
            if 'page_data' not in page:
                raise serializers.ValidationError("每个页面必须包含 page_data")
            
            page_data = page['page_data']
            if not isinstance(page_data, dict):
                raise serializers.ValidationError("page_data 必须是一个字典")
            
            if 'elements' not in page_data:
                raise serializers.ValidationError("page_data 必须包含 elements")
            
            if 'config' not in page_data:
                raise serializers.ValidationError("page_data 必须包含 config")
            
            config = page_data['config']
            if not isinstance(config, dict):
                raise serializers.ValidationError("config 必须是一个字典")
            
            required_config_fields = ['width', 'height', 'showGuideLine']
            for field in required_config_fields:
                if field not in config:
                    raise serializers.ValidationError(f"config 必须包含 {field}")

        return value

    def validate(self, data):
        """验证完整的数据"""
        if not data.get('name'):
            raise serializers.ValidationError({"name": "模板名称不能为空"})
        
        if not data.get('category'):
            raise serializers.ValidationError({"category": "必须选择分类"})
        
        if not data.get('pages'):
            raise serializers.ValidationError({"pages": "页面数据不能为空"})
        
        return data