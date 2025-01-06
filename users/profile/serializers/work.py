from rest_framework import serializers
from ..models import WorkExperience
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone

logger = logging.getLogger(__name__)

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            'id', 'company', 'position', 'department',
            'start_date', 'end_date', 'is_current',
            'description', 'achievements', 'technologies',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'company': {'required': True, 'error_messages': {'required': '请输入公司名称'}},
            'position': {'required': False},
            'department': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
            'description': {'required': False},
            'achievements': {'required': False},
            'technologies': {'required': False}
        }

    def validate(self, attrs):
        """验证数据"""
        logger.info(f"验证工作经历数据: {attrs}")
        
        # 如果设置了开始日期和结束日期,验证日期逻辑
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        is_current = attrs.get('is_current', False)
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"end_date": "结束日期不能早于开始日期"})
            
        # 如果是当前工作,清除结束日期
        if is_current:
            attrs['end_date'] = None
            
        # 如果填写了工作描述,验证长度
        description = attrs.get('description', '').strip()
        if description and len(description) < 50:
            raise serializers.ValidationError({"description": "工作描述至少需要50个字符"})
            
        return attrs

    def to_representation(self, instance):
        """自定义数据展示"""
        data = super().to_representation(instance)
        # 添加额外的展示字段
        data['duration'] = self.get_duration(instance)
        return data
        
    def get_duration(self, obj):
        """计算工作时长"""
        if not obj.start_date:
            return ''
            
        end = obj.end_date or timezone.now().date()
        duration = relativedelta(end, obj.start_date)
        
        years = duration.years
        months = duration.months
        
        if years > 0 and months > 0:
            return f"{years}年{months}个月"
        elif years > 0:
            return f"{years}年"
        elif months > 0:
            return f"{months}个月"
        else:
            return "不到1个月"
