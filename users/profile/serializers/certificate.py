from rest_framework import serializers
from ..models.certificate import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'id',
            'name',
            'issuing_authority',
            'issue_date',
            'expiry_date',
            'credential_id',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 