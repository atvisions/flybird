from django.urls import get_resolver
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from rest_framework.parsers import MultiPartParser, FormParser
import logging
import os

logger = logging.getLogger(__name__)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        """获取用户信息"""
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"获取用户信息失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '获取用户信息失败'
            }, status=500)

    def put(self, request):
        """更新用户信息"""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '更新成功',
                'data': serializer.data
            })
        return Response({
            'code': 400,
            'message': '更新失败',
            'errors': serializer.errors
        })

class AvatarUploadView(APIView):
    """头像上传接口"""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            avatar = request.FILES.get('avatar')
            if not avatar:
                return Response({
                    'code': 400,
                    'message': '请选择要上传的头像'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证文件类型
            if not avatar.content_type.startswith('image/'):
                return Response({
                    'code': 400,
                    'message': '请上传图片文件'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 直接更新用户的头像
            user = request.user
            
            # 保存前先保存旧的头像路径
            old_avatar = user.avatar.path if user.avatar else None
            
            # 更新头像
            user.avatar = avatar
            user.save()
            
            # 如果有旧头像，尝试删除
            if old_avatar and os.path.exists(old_avatar):
                try:
                    os.remove(old_avatar)
                except Exception as e:
                    logger.warning(f"删除旧头像失败: {str(e)}")
            
            # 确保返回的是字符串URL
            avatar_url = request.build_absolute_uri(user.avatar.url) if user.avatar else None
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

class BackgroundUploadView(APIView):
    """背景图上传接口"""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            background = request.FILES.get('background')
            if not background:
                return Response({
                    'code': 400,
                    'message': '请选择要上传的背景图'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证文件类型
            if not background.content_type.startswith('image/'):
                return Response({
                    'code': 400,
                    'message': '请上传图片文件'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 直接更新用户的背景图
            user = request.user
            user.background_image = background
            user.save()
            
            # 确保返回的是字符串URL
            background_url = user.background_image.url if user.background_image else None
            logger.info(f"背景图URL: {background_url}, 类型: {type(background_url)}")
            
            return Response({
                'code': 200,
                'message': '背景图上传成功',
                'data': {
                    'background': background_url
                }
            })
            
        except Exception as e:
            logger.error(f"上传背景图失败: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': '上传背景图失败'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_urls(request):
    """列出所有可用的API端点"""
    api_docs = {
        "认证相关": {
            "/api/v1/users/auth/login/password/": {
                "method": "POST",
                "description": "使用手机号和密码登录",
                "params": {
                    "phone": "手机号",
                    "password": "密码"
                }
            },
            "/api/v1/users/auth/register/": {
                "method": "POST",
                "description": "新用户注册",
                "params": {
                    "phone": "手机号",
                    "password": "密码",
                    "code": "短信验证码"
                }
            },
            "/api/v1/users/auth/sms/send/": {
                "method": "POST",
                "description": "发送短信验证码",
                "params": {
                    "phone": "手机号",
                    "scene": "场景(register/login/reset_password/change_phone)"
                }
            },
            "/api/v1/users/auth/token/refresh/": {
                "method": "POST",
                "description": "刷新访问令牌",
                "params": {
                    "refresh": "刷新令牌"
                }
            },
            "/api/v1/users/auth/logout/": {
                "method": "POST",
                "description": "退出登录",
                "auth": "需要认证",
                "params": {
                    "refresh": "刷新令牌"
                }
            }
        },
        "档案管理": {
            "/api/v1/users/profile/basic/": {
                "method": ["GET", "PUT"],
                "description": "基本信息管理",
                "auth": "需要认证",
                "fields": {
                    "name": "姓名",
                    "gender": "性别(male/female/other)",
                    "birth_date": "出生日期",
                    "location": "所在地",
                    "email": "邮箱",
                    "personal_summary": "个人简介"
                }
            },
            "/api/v1/users/profile/work-experiences/": {
                "method": ["GET", "POST"],
                "description": "工作经历管理",
                "auth": "需要认证",
                "fields": {
                    "company": "公司名称",
                    "position": "职位",
                    "department": "部门",
                    "start_date": "开始时间",
                    "end_date": "结束时间",
                    "is_current": "是否当前工作",
                    "company_description": "公司描述",
                    "responsibilities": "工作职责",
                    "achievements": "工作成果",
                    "technologies": "技术栈"
                }
            },
            "/api/v1/users/profile/educations/": {
                "method": ["GET", "POST"],
                "description": "教育经历管理",
                "auth": "需要认证",
                "fields": {
                    "school": "学校名称",
                    "major": "专业",
                    "degree": "学位",
                    "start_date": "开始时间",
                    "end_date": "结束时间",
                    "description": "描述"
                }
            },
            "/api/v1/users/profile/skills/": {
                "method": ["GET", "POST"],
                "description": "技能特长管理",
                "auth": "需要认证",
                "fields": {
                    "name": "技能名称",
                    "level": "掌握程度",
                    "description": "描述",
                    "projects": "相关项目"
                }
            },
            "/api/v1/users/profile/certificates/": {
                "method": ["GET", "POST"],
                "description": "证书资质管理",
                "auth": "需要认证",
                "fields": {
                    "name": "证书名称",
                    "type": "证书类型",
                    "issuing_authority": "发证机构",
                    "issue_date": "发证日期",
                    "expiry_date": "到期日期",
                    "description": "描述"
                }
            },
            "/api/v1/users/profile/languages/": {
                "method": ["GET", "POST"],
                "description": "语言能力管理",
                "auth": "需要认证",
                "fields": {
                    "name": "语言名称",
                    "level": "掌握程度",
                    "description": "描述"
                }
            },
            "/api/v1/users/profile/portfolios/": {
                "method": ["GET", "POST"],
                "description": "作品集管理",
                "auth": "需要认证",
                "fields": {
                    "title": "作品标题",
                    "type": "作品类型",
                    "description": "描述",
                    "url": "作品链接",
                    "highlights": "项目亮点"
                }
            },
            "/api/v1/users/profile/content-quality/": {
                "method": ["POST", "PUT"],
                "description": "AI优化档案内容",
                "auth": "需要认证",
                "post_description": "获取优化建议",
                "put_description": "应用优化建议",
                "put_params": {
                    "optimization_id": "优化建议ID"
                }
            },
            "/api/v1/users/profile/completeness/": {
                "method": "GET",
                "description": "获取档案完整度",
                "auth": "需要认证"
            }
        },
        "会员服务": {
            "/api/v1/membership/tiers/": {
                "method": "GET",
                "description": "获取会员等级列表",
                "auth": "需要认证"
            },
            "/api/v1/membership/purchase/": {
                "method": "POST",
                "description": "购买会员",
                "auth": "需要认证",
                "params": {
                    "tier_id": "会员等级ID",
                    "duration": "购买时长(monthly/quarterly/yearly)",
                    "payment_method": "支付方式(alipay/wechat)"
                }
            },
            "/api/v1/membership/check-in/": {
                "method": "POST",
                "description": "每日签到",
                "auth": "需要认证"
            },
            "/api/v1/membership/points/balance/": {
                "method": "GET",
                "description": "获取积分余额",
                "auth": "需要认证"
            },
            "/api/v1/membership/points/records/": {
                "method": "GET",
                "description": "获取积分记录",
                "auth": "需要认证"
            }
        },
        "支付相关": {
            "/api/v1/membership/notify/alipay/": {
                "method": "POST",
                "description": "支付宝支付回调",
                "auth": "不需要认证"
            },
            "/api/v1/membership/notify/alipay/return/": {
                "method": "GET",
                "description": "支付宝支付跳转",
                "auth": "不需要认证"
            }
        }
    }
    
    return Response({
        'code': 200,
        'message': '获取成功',
        'data': {
            'api_version': 'v1',
            'base_url': 'http://localhost:8000/api/v1',
            'auth_type': 'Bearer Token',
            'content_type': 'application/json',
            'endpoints': api_docs
        }
    })