from rest_framework import serializers
from django.utils import timezone
from ..models import BasicInfo
import re
import logging

logger = logging.getLogger(__name__)

class FlexibleDateField(serializers.DateField):
    """灵活的日期字段，可以处理空字符串和None"""
    
    def to_internal_value(self, value):
        """转换输入值为日期对象"""
        if not value or value == '':
            return None
        try:
            return super().to_internal_value(value)
        except (ValueError, TypeError):
            return None

class BasicInfoSerializer(serializers.ModelSerializer):
    birth_date = FlexibleDateField(required=False, allow_null=True)
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = BasicInfo
        fields = [
            'id', 'name', 'avatar', 'gender', 'birth_date',
            'phone', 'email', 'location', 'personal_summary',
            'background'
        ]
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
            'gender': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True},
            'location': {'required': False, 'allow_blank': True},
            'personal_summary': {'required': False, 'allow_blank': True},
        }
        
    def get_avatar(self, obj):
        """获取头像URL"""
        if obj.avatar:
            return obj.avatar.url
        return None
        
    def validate(self, attrs):
        """验证所有字段"""
        logger.info(f"开始验证数据: {attrs}")
        try:
            # 验证每个字段
            for field, value in attrs.items():
                logger.info(f"验证字段 {field}: {value}")
                if hasattr(self, f'validate_{field}'):
                    attrs[field] = getattr(self, f'validate_{field}')(value)
            return attrs
        except serializers.ValidationError as e:
            logger.error(f"验证失败: {e.detail}")
            raise
