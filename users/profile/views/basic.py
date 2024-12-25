from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import BasicInfoSerializer  # 只导入需要的序列化器
from ..models import BasicInfo

class BasicProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        basic_info = request.user.basic_info
        serializer = BasicInfoSerializer(basic_info)
        return Response({
            'code': 200,
            'data': serializer.data
        })

class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # 头像上传逻辑
        pass 