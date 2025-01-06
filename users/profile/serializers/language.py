from rest_framework import serializers
from ..models import Language

class LanguageSerializer(serializers.ModelSerializer):
    proficiency_display = serializers.CharField(source='get_proficiency_display', read_only=True)
    
    class Meta:
        model = Language
        fields = [
            'id',
            'name',
            'proficiency',
            'proficiency_display',
            'certification',
            'score',
            'quality_score',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

