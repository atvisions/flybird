from rest_framework import serializers
from ..models import Language

class LanguageSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = Language
        fields = [
            'id',
            'name',
            'level',
            'level_display',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 