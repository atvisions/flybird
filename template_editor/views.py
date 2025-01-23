# template_editor/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Template
from .serializers import CategorySerializer, TemplateSerializer
from .permissions import IsAdminUserOrReadOnly, CanModifyTemplate

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
    permission_classes = [IsAuthenticated, CanModifyTemplate]

    def perform_create(self, serializer):
        """创建时自动设置创建者"""
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        """根据用户权限和查询参数返回不同的查询集"""
        user = self.request.user
        queryset = Template.objects.all()

        # 基础权限过滤
        if not user.is_staff:
            queryset = queryset.filter(is_public=True) | queryset.filter(creator=user)

        # 获取查询参数
        status = self.request.query_params.get('status')
        is_public = self.request.query_params.get('is_public')
        is_recommended = self.request.query_params.get('is_recommended')
        category = self.request.query_params.get('category')

        # 应用过滤条件
        if status is not None:
            queryset = queryset.filter(status=status)
        if is_public is not None:
            is_public = is_public.lower() == 'true'
            queryset = queryset.filter(is_public=is_public)
        if is_recommended is not None:
            is_recommended = is_recommended.lower() == 'true'
            queryset = queryset.filter(is_recommended=is_recommended)
        if category:
            queryset = queryset.filter(category=category)

        return queryset

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

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞/取消点赞模板"""
        template = self.get_object()
        user = request.user
        
        if user in template.liked_by.all():
            # 取消点赞
            template.liked_by.remove(user)
            template.likes -= 1
            template.save()
            return Response({'message': '已取消点赞', 'is_liked': False})
        else:
            # 添加点赞
            template.liked_by.add(user)
            template.likes += 1
            template.save()
            return Response({'message': '点赞成功', 'is_liked': True})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_recommend(self, request, pk=None):
        """切换模板的推荐状态"""
        template = self.get_object()
        
        # 只有管理员可以设置推荐状态
        if not request.user.is_staff:
            return Response({
                'status': 'error',
                'message': '只有管理员可以设置推荐状态'
            }, status=status.HTTP_403_FORBIDDEN)
        
        template.is_recommended = not template.is_recommended
        template.save()
        
        return Response({
            'status': 'success',
            'is_recommended': template.is_recommended,
            'message': '已设为推荐' if template.is_recommended else '已取消推荐'
        })

    def retrieve(self, request, *args, **kwargs):
        """获取模板详情时增加浏览次数"""
        instance = self.get_object()
        instance.views += 1
        instance.save()
        
        # 添加当前用户是否点赞的信息
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['is_liked'] = request.user in instance.liked_by.all() if request.user.is_authenticated else False
        
        return Response(data)