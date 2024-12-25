from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.completeness import CompletenessCalculator
from ..serializers.completeness import CompletenessScoreSerializer

class ProfileCompletenessView(APIView):
    """档案完整度分析"""
    
    def get(self, request):
        calculator = CompletenessCalculator()
        result = calculator.calculate_completeness(request.user)
        
        serializer = CompletenessScoreSerializer(result)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        }) 