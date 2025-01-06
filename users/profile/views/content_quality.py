import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..services.content_quality import ContentQualityService
import uuid
from django.core.cache import cache

logger = logging.getLogger('users')

class ContentQualityView(APIView):
    """内容质量评估视图"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取内容质量评估"""
        service = ContentQualityService(request.user)
        return Response(service.analyze_content())
    
    def post(self, request):
        """获取优化预览"""
        service = ContentQualityService(request.user)
        result = service.preview_optimization()
        
        if result['code'] == 200:
            # 生成优化ID并缓存结果
            optimization_id = str(uuid.uuid4())
            cache.set(
                f"profile_optimization_{optimization_id}",
                result['data'],
                timeout=3600  # 1小时过期
            )
            result['data']['optimization_id'] = optimization_id
            
        return Response(result)
    
    def put(self, request):
        """应用优化结果"""
        optimization_id = request.data.get('optimization_id')
        if not optimization_id:
            return Response({
                'code': 400,
                'message': '缺少optimization_id',
                'data': None
            })
            
        service = ContentQualityService(request.user)
        return Response(service.apply_optimization(optimization_id)) 