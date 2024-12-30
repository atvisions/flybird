from django.core.cache import cache
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

from ..models import JobIntention
from ..serializers.intention import JobIntentionSerializer
from ..serializers.completeness import CompletenessScoreSerializer
from ..services.completeness import CompletenessCalculator

logger = logging.getLogger(__name__)

class JobIntentionView(APIView):
    def get(self, request):
        """获取求职意向"""
        try:
            intention = JobIntention.objects.get(user=request.user)
            serializer = JobIntentionSerializer(intention)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except JobIntention.DoesNotExist:
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': None
            })
        except Exception as e:
            logger.error(f"获取求职意向失败: {str(e)}")
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """更新求职意向"""
        try:
            with transaction.atomic():
                intention, created = JobIntention.objects.get_or_create(user=request.user)
                serializer = JobIntentionSerializer(intention, data=request.data, partial=True)
                
                if serializer.is_valid():
                    intention = serializer.save()
                    
                    try:
                        # 更新完整度分数
                        calculator = CompletenessCalculator(request.user)
                        completeness_data = calculator.get_completeness()
                        logger.info(f"完整度数据: {completeness_data}")
                        
                        # 只取需要的数据
                        if isinstance(completeness_data, dict) and 'data' in completeness_data:
                            completeness_data = completeness_data['data']
                        
                        # 清除缓存
                        cache_key = f'completeness_{request.user.id}'
                        cache.delete(cache_key)
                        
                        return Response({
                            'code': 200,
                            'message': '保存成功',
                            'data': {
                                'intention': serializer.data,
                                'completeness': completeness_data
                            }
                        })
                    except Exception as e:
                        # 如果计算完整度失败，至少返回保存成功的数据
                        logger.error(f"计算完整度失败: {str(e)}")
                        return Response({
                            'code': 200,
                            'message': '保存成功，但完整度计算失败',
                            'data': serializer.data
                        })
                    
                return Response({
                    'code': 400,
                    'message': '数据验证失败',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"保存求职意向失败: {str(e)}")
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)