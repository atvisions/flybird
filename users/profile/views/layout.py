from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import ProfileLayout
from ..serializers import ProfileLayoutSerializer
import logging

logger = logging.getLogger('users')

class ProfileLayoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取档案布局配置"""
        try:
            logger.info(f"获取用户布局 - 用户: {request.user.phone}")
            
            # 获取或创建布局
            layout, created = ProfileLayout.objects.get_or_create(
                user=request.user,
                defaults={'layout': ProfileLayout.DEFAULT_LAYOUT}
            )
            
            # 确保有默认布局且不包含 basic_info
            if not layout.layout or 'basic_info' in layout.layout:
                layout.layout = ProfileLayout.DEFAULT_LAYOUT.copy()
                layout.save()
            
            logger.info(f"布局数据: {layout.layout}")
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'layout': layout.layout
                }
            })
        except Exception as e:
            logger.error(f"获取布局失败: {str(e)}")
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        """更新布局配置"""
        try:
            logger.info(f"更新用户布局 - 用户: {request.user.phone}")
            logger.info(f"请求数据: {request.data}")
            
            layout, created = ProfileLayout.objects.get_or_create(
                user=request.user,
                defaults={'layout': ProfileLayout.DEFAULT_LAYOUT}
            )
            
            # 更新布局，但排除 basic_info
            new_layout = request.data.copy()
            if 'basic_info' in new_layout:
                del new_layout['basic_info']
                
            current_layout = layout.layout.copy()
            current_layout.update(new_layout)
            
            # 使用 update_or_create 来确保只有一条记录
            layout, _ = ProfileLayout.objects.update_or_create(
                user=request.user,
                defaults={'layout': current_layout}
            )
            
            logger.info(f"更新后的布局: {layout.layout}")
            
            return Response({
                'code': 200,
                'message': '更新成功',
                'data': {
                    'layout': layout.layout
                }
            })
        except Exception as e:
            logger.error(f"更新布局失败: {str(e)}")
            return Response({
                'code': 500,
                'message': '更新失败',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取档案布局配置"""
        try:
            logger.info(f"获取用户布局 - 用户: {request.user.phone}")
            
            # 获取或创建布局
            layout, created = ProfileLayout.objects.get_or_create(
                user=request.user
            )
            
            # 确保有默认布局
            if not layout.layout:
                layout.layout = ProfileLayout.DEFAULT_LAYOUT.copy()
                layout.save()
            
            logger.info(f"布局数据: {layout.layout}")
            
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'layout': layout.layout
                }
            })
        except Exception as e:
            logger.error(f"获取布局失败: {str(e)}")
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        """更新布局配置"""
        try:
            logger.info(f"更新用户布局 - 用户: {request.user.phone}")
            logger.info(f"请求数据: {request.data}")
            
            layout, created = ProfileLayout.objects.get_or_create(
                user=request.user,
                defaults={'layout': ProfileLayout.DEFAULT_LAYOUT}
            )
            
            # 更新布局
            current_layout = layout.layout.copy()
            current_layout.update(request.data)
            
            # 使用 update_or_create 来确保只有一条记录
            layout, _ = ProfileLayout.objects.update_or_create(
                user=request.user,
                defaults={'layout': current_layout}
            )
            
            logger.info(f"更新后的布局: {layout.layout}")
            
            return Response({
                'code': 200,
                'message': '更新成功',
                'data': {
                    'layout': layout.layout
                }
            })
        except Exception as e:
            logger.error(f"更新布局失败: {str(e)}")
            return Response({
                'code': 500,
                'message': '更新失败',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 