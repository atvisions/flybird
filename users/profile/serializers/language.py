from rest_framework import serializers
from ..models.language import Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ['user']
        read_only_fields = ['created_at', 'updated_at']
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['proficiency_display'] = instance.get_proficiency_display()
        return ret 