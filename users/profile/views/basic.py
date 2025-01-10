# users/profile/views/basic.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from ..serializers import BasicInfoSerializer
from ..models import BasicInfo
import logging

logger = logging.getLogger(__name__)

class BasicProfileView(APIView):
    """基本信息接口"""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get(self, request):
        """获取基本信息"""
        try:
            basic_info = request.user.basic_info
            serializer = BasicInfoSerializer(basic_info)
            
            # 记录返回的数据
            logger.info(f"基本信息数据: {serializer.data}")
            user = request.user
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'user': {
                        'uid': user.uid,
                        'username': user.username,
                        'phone': user.phone
                    },
                    'basic_info': serializer.data
                }
            })
        except Exception as e:
            logger.error(f"获取基本信息失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '获取基本信息失败'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """创建/更新基本信息"""
        try:
            logger.info(f"接收到的数据: {request.data}")
            
            basic_info, created = BasicInfo.objects.get_or_create(user=request.user)
            serializer = BasicInfoSerializer(
                instance=basic_info,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': '保存成功',
                    'data': serializer.data
                })
            
            # 格式化验证错误信息
            errors = {}
            for field, error_list in serializer.errors.items():
                errors[field] = [str(error) for error in error_list]
            
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"保存失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AvatarUploadView(APIView):
    """头像上传接口"""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            logger.info(f"收到的文件数据: {request.FILES}")
            avatar = request.FILES.get('avatar')
            if not avatar:
                logger.error("未找到头像文件，请求FILES内容：%s", request.FILES)
                return Response({
                    'code': 400,
                    'message': '请选择要上传的头像'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证文件类型
            if not avatar.content_type.startswith('image/'):
                logger.error(f"文件类型错误: {avatar.content_type}")
                return Response({
                    'code': 400,
                    'message': '请上传图片文件'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取或创建基本信息
            basic_info, _ = BasicInfo.objects.get_or_create(user=request.user)
            
            # 保存新头像
            basic_info.avatar = avatar
            basic_info.save()
            
            # 确保返回的是字符串URL
            avatar_url = basic_info.avatar.url if basic_info.avatar else None
            logger.info(f"头像URL: {avatar_url}, 类型: {type(avatar_url)}")
            
            return Response({
                'code': 200,
                'message': '头像上传成功',
                'data': {
                    'avatar': avatar_url
                }
            })
            
        except Exception as e:
            logger.error(f"上传头像失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '上传头像失败'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   