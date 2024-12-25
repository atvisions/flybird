from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.completeness import CompletenessCalculator

class ProfileCompletenessView(APIView):
    """档案完整度分析"""
    
    def get(self, request):
        try:
            calculator = CompletenessCalculator(user=request.user)
            result = calculator.get_completeness()
            
            return Response(result)
            
        except Exception as e:
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 