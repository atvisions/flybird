from rest_framework import serializers
from ..models.intention import JobIntention

class JobIntentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobIntention
        exclude = ['user']
        read_only_fields = ['updated_at']
        
    def to_representation(self, instance):
        """自定义数据展示"""
        ret = super().to_representation(instance)
        # 添加选项的显示值
        ret['status_display'] = instance.get_status_display()
        ret['salary_expectation_display'] = instance.get_salary_expectation_display()
        return ret 