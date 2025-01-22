# template_editor/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Template
from .serializers import CategorySerializer, TemplateSerializer
from .permissions import IsAdminUserOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    """
    模版分类视图集
    只允许管理员创建、修改和删除分类
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    
    def get_queryset(self):
        """返回按照排序字段排序的分类列表"""
        return Category.objects.all().order_by('sort_order', 'id')

class TemplateViewSet(viewsets.ModelViewSet):
    """
    模版视图集
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """创建时自动设置创建者"""
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        """根据用户权限返回不同的查询集"""
        user = self.request.user
        if user.is_staff:
            return Template.objects.all()
        return Template.objects.filter(is_public=True) | Template.objects.filter(creator=user)

    @action(detail=True, methods=['post'])
    def add_page(self, request, pk=None):
        """添加新页面"""
        template = self.get_object()
        try:
            page_index = template.add_page()
            return Response({
                'status': 'success',
                'page_index': page_index
            })
        except ValueError as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_page(self, request, pk=None):
        """更新页面"""
        template = self.get_object()
        page_index = request.data.get('page_index')
        page_data = request.data.get('page_data')
        
        try:
            template.update_page(page_index, page_data)
            return Response({'status': 'success'})
        except ValueError as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_page(self, request, pk=None):
        """删除页面"""
        template = self.get_object()
        page_index = request.data.get('page_index')
        
        try:
            template.delete_page(page_index)
            return Response({'status': 'success'})
        except ValueError as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_page(self, request, pk=None):
        """获取指定页面数据"""
        template = self.get_object()
        page_index = request.query_params.get('page_index', 0)
        
        try:
            page_index = int(page_index)
            if not 0 <= page_index < len(template.pages):
                raise ValueError('无效的页面索引')
            
            return Response({
                'status': 'success',
                'page_data': template.pages[page_index]
            })
        except (ValueError, IndexError) as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_all_pages(self, request, pk=None):
        """获取所有页面数据"""
        template = self.get_object()
        return Response({
            'status': 'success',
            'pages': template.pages
        })