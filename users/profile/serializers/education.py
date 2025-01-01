from rest_framework import serializers
from ..models.education import Education

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id',
            'school',
            'major',
            'degree',
            'start_date',
            'end_date',
            'is_current',
            'description',
            'achievements',  
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        验证日期逻辑：
        1. 如果是在读，结束日期应为空
        2. 如果不是在读，结束日期不能早于开始日期
        """
        if data.get('is_current'):
            data['end_date'] = None
        elif data.get('end_date') and data['end_date'] < data['start_date']:
            raise serializers.ValidationError('结束日期不能早于开始日期')
        return data
