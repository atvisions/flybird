class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInfo
        fields = [
            'id', 'name', 'avatar', 'background', 'gender', 'birth_date',
            'phone', 'email', 'location', 'personal_summary'
        ] 