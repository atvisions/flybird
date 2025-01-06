from rest_framework import serializers
from ..models import Portfolio

class PortfolioSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Portfolio
        fields = [
            'id',
            'title',
            'type',
            'type_display',
            'description',
            'url',
            'image',
            'highlights',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 