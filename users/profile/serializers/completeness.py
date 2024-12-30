from rest_framework import serializers

class DimensionScoreSerializer(serializers.Serializer):
    score = serializers.FloatField(required=False, allow_null=True)
    weight = serializers.FloatField(required=False, allow_null=True)
    weighted_score = serializers.FloatField(required=False, allow_null=True)

class CompletenessScoreSerializer(serializers.Serializer):
    total_score = serializers.IntegerField(required=False)
    total_detail = serializers.DictField(
        child=DimensionScoreSerializer(),
        required=False
    )
    level = serializers.CharField(required=False)
    
    # 各维度得分
    basic_dimension = DimensionScoreSerializer(required=False)
    experience_dimension = DimensionScoreSerializer(required=False)
    capability_dimension = DimensionScoreSerializer(required=False)
    achievement_dimension = DimensionScoreSerializer(required=False)
    
    # 文字专业度评分
    content_professionalism = DimensionScoreSerializer(required=False)
    
    # 改进建议
    improvement_suggestions = serializers.ListField(
        child=serializers.DictField(),
        required=False
    ) 