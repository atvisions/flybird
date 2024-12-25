from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Skill
from ..serializers import SkillSerializer
import logging

logger = logging.getLogger(__name__)

class SkillView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取技能特长列表"""
        try:
            skills = request.user.skills.all()
            serializer = SkillSerializer(skills, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in SkillView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """添加技能特长"""
        try:
            serializer = SkillSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({
                    'code': 200,
                    'message': '添加成功',
                    'data': serializer.data
                })
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in SkillView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SkillDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return user.skills.filter(pk=pk).first()
    
    def get(self, request, pk):
        """获取技能特长详情"""
        try:
            skill = self.get_object(pk, request.user)
            if not skill:
                return Response({
                    'code': 404,
                    'message': '技能特长不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = SkillSerializer(skill)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error in SkillDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        """更新技能特长"""
        try:
            skill = self.get_object(pk, request.user)
            if not skill:
                return Response({
                    'code': 404,
                    'message': '技能特长不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = SkillSerializer(skill, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'code': 200,
                    'message': '更新成功',
                    'data': serializer.data
                })
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in SkillDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """删除技能特长"""
        try:
            skill = self.get_object(pk, request.user)
            if not skill:
                return Response({
                    'code': 404,
                    'message': '技能特长不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            skill.delete()
            return Response({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            logger.error(f"Error in SkillDetailView: {str(e)}", exc_info=True)
            return Response({
                'code': 500,
                'message': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 