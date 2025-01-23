from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Q
from .models import Resume
from .serializers import ResumeSerializer

# Create your views here.

class ResumeViewSet(viewsets.ModelViewSet):
    """简历视图集"""
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """获取查询集"""
        user = self.request.user
        # 返回用户自己的简历和公开的简历
        return Resume.objects.filter(
            Q(creator=user) | Q(is_public=True)
        ).select_related('creator', 'template')

    def perform_create(self, serializer):
        """创建时设置创建者"""
        print('创建简历的数据:', serializer.validated_data)  # 添加日志打印
        try:
            serializer.save(creator=self.request.user)
        except Exception as e:
            print('创建简历失败:', str(e))  # 添加错误日志
            raise

    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """增加浏览次数"""
        resume = self.get_object()
        resume.view_count = F('view_count') + 1
        resume.save()
        return Response({'status': 'success'})

    @action(detail=True, methods=['post'])
    def increment_download(self, request, pk=None):
        """增加下载次数"""
        resume = self.get_object()
        resume.download_count = F('download_count') + 1
        resume.save()
        return Response({'status': 'success'})

    @action(detail=False, methods=['get'])
    def my_resumes(self, request):
        """获取我的简历列表"""
        queryset = self.get_queryset().filter(creator=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
