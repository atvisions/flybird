from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from .models import ResumeTemplate, Resume, TemplateCategory, Component, ComponentCategory
from .serializers import (
    ResumeTemplateSerializer, ResumeSerializer,
    TemplateCategorySerializer, ComponentSerializer,
    ComponentCategorySerializer, ComponentListSerializer, ComponentDetailSerializer
)
from .permissions import IsTemplateCreator

class TemplateCategoryViewSet(viewsets.ModelViewSet):
    queryset = TemplateCategory.objects.filter(parent=None, is_active=True)
    serializer_class = TemplateCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ResumeTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'tags']

    def get_queryset(self):
        """
        根据用户权限返回不同的模板列表：
        - 普通用户只能看到已审核通过的免费模板
        - VIP用户可以看到所有已审核通过的模板
        - 管理员可以看到所有模板
        """
        queryset = ResumeTemplate.objects.all().order_by('-created_at')
        
        # 分类过滤
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # 标签过滤
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)

        if self.request.user.is_staff:
            return queryset
        
        if self.request.user.is_vip:
            return queryset.filter(status='approved')
        
        return queryset.filter(status='approved', is_vip=False)

    def list(self, request, *args, **kwargs):
        """重写列表方法，确保返回的数据包含 id"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """创建模板时自动设置创建者"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """获取模板详情时增加浏览次数"""
        instance = self.get_object()
        instance.views_count = F('views_count') + 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, pk=None):
        """提交模板审核"""
        template = self.get_object()
        template.status = 'pending'
        template.save()
        return Response({'status': 'submitted'})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """审核通过模板（仅管理员）"""
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        template = self.get_object()
        template.status = 'approved'
        template.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """拒绝模板（仅管理员）"""
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        template = self.get_object()
        template.status = 'rejected'
        template.save()
        return Response({'status': 'rejected'})

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """复制模板"""
        template = self.get_object()
        new_template = ResumeTemplate.objects.create(
            name=f"{template.name} - 副本",
            description=template.description,
            creator=request.user,
            category=template.category,
            components=template.components,
            layout=template.layout,
            theme=template.theme,
            is_vip=False,  # 复制的模板默认为非VIP
            status='pending'  # 需要重新审核
        )
        return Response(ResumeTemplateSerializer(new_template).data)

    @action(detail=True, methods=['patch'])
    def update_components(self, request, pk=None):
        """更新模板组件配置"""
        template = self.get_object()
        if not request.user.is_staff and template.creator != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        template.components = request.data.get('components', template.components)
        template.save()
        return Response(ResumeTemplateSerializer(template).data)

    @action(detail=True, methods=['patch'])
    def update_layout(self, request, pk=None):
        """更新模板布局配置"""
        template = self.get_object()
        if not request.user.is_staff and template.creator != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        template.layout = request.data.get('layout', template.layout)
        template.save()
        return Response(ResumeTemplateSerializer(template).data)

    @action(detail=True, methods=['patch'])
    def update_theme(self, request, pk=None):
        """更新模板主题配置"""
        template = self.get_object()
        if not request.user.is_staff and template.creator != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        template.theme = request.data.get('theme', template.theme)
        template.save()
        return Response(ResumeTemplateSerializer(template).data)

    @action(detail=True, methods=['post'])
    def preview(self, request, pk=None):
        """生成模板预览"""
        template = self.get_object()
        # TODO: 实现预览生成逻辑
        return Response({'preview_url': 'url_to_preview'})

    @action(detail=False, methods=['get'])
    def system_templates(self, request):
        """获取系统预设模板"""
        queryset = self.get_queryset().filter(
            creator__is_staff=True,
            status='approved'
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 检查用户是否有权限使用该模板
        template_id = self.request.data.get('template_id')
        template = ResumeTemplate.objects.get(id=template_id)
        
        if template.is_vip and not self.request.user.is_vip:
            raise PermissionError("该模板仅VIP用户可用")
        
        # 增加模板使用次数
        template.used_count = F('used_count') + 1
        template.save()
            
        serializer.save(user=self.request.user) 

class ComponentCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """组件分类视图集"""
    queryset = ComponentCategory.objects.filter(is_active=True)
    serializer_class = ComponentCategorySerializer
    permission_classes = [permissions.AllowAny]  # 允许所有用户访问
    
    @action(detail=False, methods=['get'])
    def main_categories(self, request):
        """获取主分类（布局、组件、档案）"""
        categories = ComponentCategory.objects.filter(
            code__in=['layout', 'component', 'file'],
            is_active=True
        ).order_by('sort_order')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def components(self, request, pk=None):
        """获取分类下的组件列表"""
        category = self.get_object()
        components = Component.objects.filter(category=category, is_system=True)
        serializer = ComponentListSerializer(components, many=True)
        return Response(serializer.data)

class ComponentViewSet(viewsets.ReadOnlyModelViewSet):
    """组件视图集"""
    queryset = Component.objects.filter(is_system=True)
    permission_classes = [permissions.AllowAny]  # 允许所有用户访问
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ComponentListSerializer
        return ComponentDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset 