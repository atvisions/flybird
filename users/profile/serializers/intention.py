from rest_framework import serializers
from ..models import JobIntention
import logging

logger = logging.getLogger(__name__)

class JobIntentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobIntention
        fields = [
            'id', 'job_type', 'job_status', 'expected_salary',
            'expected_city', 'industries'
        ]
        extra_kwargs = {
            'job_type': {'required': False, 'allow_blank': True},
            'job_status': {'required': False, 'allow_blank': True},
            'expected_salary': {'required': False, 'allow_blank': True},
            'expected_city': {'required': False, 'allow_blank': True},
            'industries': {'required': False, 'allow_blank': True},
        }

    def validate(self, attrs):
        """验证数据"""
        logger.info(f"验证求职意向数据: {attrs}")
        return attrs

    def update(self, instance, validated_data):
        """更新实例"""
        logger.info(f"更新求职意向: {validated_data}")
        try:
            for field, value in validated_data.items():
                setattr(instance, field, value)
            instance.save()
            return instance
        except Exception as e:
            logger.error(f"更新求职意向失败: {str(e)}")
            raise