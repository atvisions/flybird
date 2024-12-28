class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            'id', 'company', 'position', 'department',
            'start_date', 'end_date', 'is_current',
            'company_description', 'responsibilities', 'achievements',
            'created_at', 'updated_at'
        ] 