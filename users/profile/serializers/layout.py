from rest_framework import serializers
from ..models.layout import ProfileLayout

class ProfileLayoutSerializer(serializers.ModelSerializer):
    available_modules = serializers.SerializerMethodField()
    
    class Meta:
        model = ProfileLayout
        exclude = ['user']
        read_only_fields = ['updated_at']
        
    def get_available_modules(self, obj):
        """获取所有可用模块"""
        return obj.available_modules

    def validate_active_modules(self, value):
        """验证激活的模块"""
        # 确保包含所有核心模块
        core_modules = [m[0] for m in ProfileLayout.CORE_MODULES]
        for module in core_modules:
            if module not in value:
                raise serializers.ValidationError(f"核心模块 '{module}' 不能被禁用")
        
        # 验证其他模块是否有效
        all_modules = dict(ProfileLayout.AVAILABLE_MODULES).keys()
        invalid_modules = [m for m in value if m not in all_modules]
        if invalid_modules:
            raise serializers.ValidationError(f"无效的模块: {', '.join(invalid_modules)}")
        return value

    def validate_module_order(self, value):
        """验证模块顺序"""
        # 确保所有排序的模块都在激活列表中
        active_modules = self.initial_data.get('active_modules', self.instance.active_modules if self.instance else [])
        invalid_modules = [m for m in value if m not in active_modules]
        if invalid_modules:
            raise serializers.ValidationError(f"未激活的模块不能排序: {', '.join(invalid_modules)}")
        return value 