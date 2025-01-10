from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'uid', 'username', 'phone', 'email', 'avatar', 
                 'background_image', 'position', 'bio', 'is_vip', 'is_staff']
        read_only_fields = ['id', 'uid', 'phone', 'email'] 
