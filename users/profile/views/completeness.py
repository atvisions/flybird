import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..services.completeness import CompletenessCalculator

logger = logging.getLogger('users')

class ProfileCompletenessView(APIView):
    """档案完整度视图"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            calculator = CompletenessCalculator(request.user)
            # 计算各维度得分
            basic_score = float(calculator.calculate_basic_score())
            experience_score = float(calculator.calculate_experience_score())
            capability_score = float(calculator.calculate_capability_score())
            achievement_score = float(calculator.calculate_achievement_score())
            
            # 计算总分
            total_score = (
                basic_score * 0.4 +
                experience_score * 0.3 +
                capability_score * 0.2 +
                achievement_score * 0.1
            )
            
            # 更新数据库中的分数
            calculator.score.basic_dimension = basic_score
            calculator.score.experience_dimension = experience_score
            calculator.score.ability_dimension = capability_score
            calculator.score.achievement_dimension = achievement_score
            calculator.score.total_score = total_score
            calculator.score.save()
            
            result = {
                'code': 200,
                'message': '获取成功',
                'data': {
                    'total_score': round(total_score, 1),
                    'dimensions': {
                        'basic_info': {
                            'score': float(basic_score),
                            'weight': 0.4,
                            'weighted_score': round(basic_score * 0.4, 1)
                        },
                        'experience': {
                            'score': float(experience_score),
                            'weight': 0.3,
                            'weighted_score': round(experience_score * 0.3, 1)
                        },
                        'capability': {
                            'score': float(capability_score),
                            'weight': 0.2,
                            'weighted_score': round(capability_score * 0.2, 1)
                        },
                        'achievement': {
                            'score': float(achievement_score),
                            'weight': 0.1,
                            'weighted_score': round(achievement_score * 0.1, 1)
                        }
                    },
                    'suggestions': calculator.get_improvement_suggestions()
                }
            }
            
            return Response(result)
            
        except Exception as e:
            logger.error(f"获取档案完整度失败: {str(e)}")
            return Response(
                {
                    'code': 500,
                    'message': '获取档案完整度失败',
                    'data': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 