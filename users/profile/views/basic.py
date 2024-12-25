# users/profile/views/basic.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from ..serializers import BasicInfoSerializer
from ..models import BasicInfo

class BasicProfileView(APIView):
    """基本信息接口"""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get(self, request):
        """获取基本信息"""
        basic_info = request.user.basic_info
        serializer = BasicInfoSerializer(basic_info)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
    
    def post(self, request):
        """创建/更新基本信息"""
        print("收到的数据:", request.data)  # 调试日志
        
        try:
            basic_info = request.user.basic_info
            serializer = BasicInfoSerializer(
                instance=basic_info,
                data=request.data,
                partial=True
            )
        except BasicInfo.DoesNotExist:
            serializer = BasicInfoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'code': 200,
                'message': '保存成功',
                'data': serializer.data
            })
        
        print("验证错误:", serializer.errors)  # 调试日志
        return Response({
            'code': 400,
            'message': '数据验证失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AvatarUploadView(APIView):
    """头像上传接口"""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        """上传头像"""
        try:
            basic_info = request.user.basic_info
            if 'avatar' not in request.FILES:
                return Response({
                    'code': 400,
                    'message': '请选择要上传的头像',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
                
            basic_info.avatar = request.FILES['avatar']
            basic_info.save()
            
            return Response({
                'code': 200,
                'message': '头像上传成功',
                'data': {
                    'avatar_url': basic_info.avatar.url if basic_info.avatar else None
                }
            })
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'头像上传失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)