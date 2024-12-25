from rest_framework import serializers

class DimensionScoreSerializer(serializers.Serializer):
    score = serializers.FloatField()
    weight = serializers.FloatField()
    weighted_score = serializers.FloatField()

class CompletenessScoreSerializer(serializers.Serializer):
    total_score = serializers.IntegerField()
    total_detail = serializers.DictField(
        child=DimensionScoreSerializer()
    )
    level = serializers.CharField()
    
    # 各维度得分
    basic_dimension = DimensionScoreSerializer()
    experience_dimension = DimensionScoreSerializer()
    capability_dimension = DimensionScoreSerializer()
    achievement_dimension = DimensionScoreSerializer()
    
    # 文字专业度评分
    content_professionalism = DimensionScoreSerializer()
    
    # 改进建议
    improvement_suggestions = serializers.ListField(
        child=serializers.DictField()
    ) 